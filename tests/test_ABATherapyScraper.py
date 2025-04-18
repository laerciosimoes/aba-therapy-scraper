import unittest
from unittest.mock import MagicMock, patch
import pathlib
import tempfile

# Import the classes to test.
from scrapper.ABATherapyScraper import ABATherapyScraper


# Define a fake WebElement that simulates Selenium's element.
class FakeWebElement(MagicMock):
    def __init__(self, text="", attributes=None, **kwargs):
        super().__init__(**kwargs)
        self._text = text
        self._attributes = attributes if attributes is not None else {}

    @property
    def text(self) -> str:
        return self._text

    def get_attribute(self, name: str) -> str:
        return self._attributes.get(name, "")


# Define a fake driver that simulates the Selenium WebDriver.
class FakeDriver:
    def __init__(self):
        self.calls = []

    def get(self, url: str) -> None:
        self.calls.append(("get", url))

    def maximize_window(self) -> None:
        self.calls.append(("maximize_window", None))

    def find_element(self, by, value):
        # If looking for the cookie banner, simulate that it is found.
        if by == "id" and value == "hs-eu-cookie-confirmation-inner":
            return FakeWebElement(text="Cookie Banner")
        # If searching for no-results element, simulate not found.
        if by == "class name" and value == "dp-dfg-no-results":
            raise Exception("Not Found")
        # For "city-state" we return a fake element.
        if by == "class name" and value == "city-state":
            return FakeWebElement(text="Test City")
        # For the article title
        if by == "css selector" and value == "h3.entry-title a":
            return FakeWebElement(
                text="Test Title", attributes={"href": "http://example.com"}
            )
        return FakeWebElement(text="Generic")

    def find_elements(self, by, value):
        if by == "class name" and value == "dp-dfg-items":
            # Create a fake container that returns a fake article.
            fake_container = FakeWebElement()
            fake_article = FakeWebElement()
            # Override the container's find_elements to return a list with a single fake article.
            fake_container.find_elements = MagicMock(return_value=[fake_article])
            # For the fake article, define find_element to return expected fake elements.
            fake_article.find_element = MagicMock(
                side_effect=lambda b, v: (
                    FakeWebElement(
                        text="Test Title", attributes={"href": "http://example.com"}
                    )
                    if (b == "css selector" and v == "h3.entry-title a")
                    else (
                        FakeWebElement(text="Test City")
                        if (b == "class name" and v == "city-state")
                        else FakeWebElement(text="Generic")
                    )
                )
            )
            return [fake_container]
        return []

    def execute_script(self, script, element):
        self.calls.append(("execute_script", script, element))

    def quit(self):
        self.calls.append(("quit", None))


# Create a fake ChromeDriverManager that returns our FakeDriver.
class FakeChromeDriverManager:
    def __init__(self):
        self.driver = FakeDriver()
        self.wait = MagicMock()  # For these tests we do not rely on real waits.

    def quit(self):
        self.driver.quit()


class TestABATherapyScraper(unittest.TestCase):
    def setUp(self) -> None:
        # Create a fake driver manager and instantiate the scraper.
        self.fake_manager = FakeChromeDriverManager()
        self.scraper = ABATherapyScraper(self.fake_manager)

    def test_get_page_url_first_page(self) -> None:
        url = self.scraper.get_page_url(1)
        self.assertEqual(url, self.scraper.BASE_URL)

    def test_get_page_url_other_pages(self) -> None:
        page_num = 3
        url = self.scraper.get_page_url(page_num)
        expected = f"{self.scraper.BASE_URL}page/{page_num}/"
        self.assertEqual(url, expected)

    @patch("time.sleep", return_value=None)
    def test_scrape_page_adds_contacts(self, _mock_sleep) -> None:
        """
        Test that scrape_page processes the fake container and adds a contact.
        """
        result = self.scraper.scrape_page()
        self.assertTrue(result)
        self.assertGreater(len(self.scraper.contacts), 0)
        contact = self.scraper.contacts[0]
        self.assertIn("Name", contact)
        self.assertIn("Url", contact)
        self.assertIn("Location", contact)

    @patch("time.sleep", return_value=None)
    def test_save_contacts_to_csv(self, _mock_sleep) -> None:
        """
        Test that save_contacts_to_csv writes a CSV file with the expected headers.
        """
        # Populate contacts with a sample record.
        self.scraper.contacts = [
            {"Name": "Test Name", "Url": "http://example.com", "Location": "Test City"}
        ]
        # Use a temporary directory for writing the CSV.
        with tempfile.TemporaryDirectory() as tmpdirname:
            original_path = pathlib.Path

            # Define a fake Path function that returns a temporary directory when
            # the input is "data", otherwise behaves normally.
            def fake_path(*args, **kwargs):
                if args and args[0] == "data":
                    return original_path(tmpdirname)
                return original_path(*args, **kwargs)

            # Patch the pathlib.Path used in the ABATherapyScraper module.
            with patch(
                "scrapper.ABATherapyScraper.pathlib.Path", side_effect=fake_path
            ):
                self.scraper.save_contacts_to_csv()
                csv_file = original_path(tmpdirname) / "contacts_list.csv"
                self.assertTrue(csv_file.exists())
                # Read the file to check that it contains the expected CSV headers.
                with open(csv_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.assertIn("Name,Url,Location", content)


if __name__ == "__main__":
    unittest.main()
