import unittest
from unittest.mock import patch, MagicMock
from scrapper.driverManager import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


class TestChromeDriverManager(unittest.TestCase):
    @patch("scrapper.driverManager.webdriver.Chrome")
    def test_initialization(self, mock_chrome):
        """
        Test that ChromeDriverManager initializes the WebDriver properly,
        maximizes the window, and sets up the WebDriverWait instance.
        """
        # Create a fake driver that will be returned by webdriver.Chrome
        fake_driver = MagicMock()
        mock_chrome.return_value = fake_driver

        # Initialize ChromeDriverManager with headless enabled.
        manager = ChromeDriverManager(headless=True, wait_time=10)

        # Check that webdriver.Chrome was called with proper options.
        mock_chrome.assert_called_once()
        # Verify the fake driver's maximize_window method was called.
        fake_driver.maximize_window.assert_called_once()

        # Check that the wait attribute is a WebDriverWait instance associated with fake_driver.
        self.assertIsInstance(manager.wait, WebDriverWait)
        self.assertEqual(manager.wait._driver, fake_driver)

    @patch("scrapper.driverManager.webdriver.Chrome")
    def test_quit(self, mock_chrome):
        """
        Test that calling quit() on ChromeDriverManager calls the driver's quit method.
        """
        # Create a fake driver
        fake_driver = MagicMock()
        mock_chrome.return_value = fake_driver

        manager = ChromeDriverManager(headless=False, wait_time=10)
        manager.quit()

        # Verify that the driver's quit() method was called exactly once.
        fake_driver.quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
