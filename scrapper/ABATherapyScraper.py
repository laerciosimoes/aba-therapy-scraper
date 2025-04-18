#!/usr/bin/env python3
import csv
import re
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scrapper.driverManager import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement

class ABATherapyScraper:
    """
    A web scraper for the ABA Therapy Directory that extracts contact articles.

    The scraper navigates through pages of the ABA Therapy Directory and extracts article details
    (Name, URL, and Location) from the contact cards until at least 100 contacts are collected
    or no more results are available.
    """

    BASE_URL: str = "https://www.bhcoe.org/aba-therapy-directory/"

    def __init__(self, driver_manager: ChromeDriverManager) -> None:
        """
        Initializes the scraper with a ChromeDriverManager instance.

        :param driver_manager: An instance of ChromeDriverManager.
        """
        self.driver_manager: ChromeDriverManager = driver_manager
        self.driver: webdriver.Chrome = driver_manager.driver
        self.wait: WebDriverWait = driver_manager.wait
        self.contacts: list[dict] = []
        self.page: int = 1

    def get_page_url(self, page_number: int) -> str:
        """
        Construct the URL for a given page number.

        For the first page, the BASE_URL is returned directly.
        For subsequent pages, a page number is appended to the BASE_URL.

        :param page_number: Integer representing the desired page number.
        :return: A formatted URL string pointing to the specified page.
        """
        if page_number == 1:
            return self.BASE_URL
        else:
            return f"{self.BASE_URL}page/{page_number}/"

    def hide_cookie_banner(self) -> None:
        """
        Hides the cookie confirmation banner if it is present.
        """
        try:
            cookie_banner = self.driver.find_element(
                By.ID, "hs-eu-cookie-confirmation-inner"
            )
            self.driver.execute_script(
                "arguments[0].style.display = 'none';", cookie_banner
            )
        except Exception:
            print("Cookie banner not found, proceeding...")

    def scrape_page(self) -> bool:
        """
        Loads a page and extracts contact articles from it.

        The method navigates to the specified page, hides the cookie banner,
        checks for "no results", and then processes containers of articles to extract details.

        :return: True if the page was processed; False if there are no more results.
        """
        url: str = self.get_page_url(self.page)
        print(f"Scraping page {self.page}: {url}")
        self.driver.get(url)
        time.sleep(2)  # Allow page to load

        # Hide cookie banner if present.
        self.hide_cookie_banner()

        # If an element indicating 'no results' is displayed, break the loop.
        try:
            no_results = self.driver.find_element(By.CLASS_NAME, "dp-dfg-no-results")
            if no_results.is_displayed():
                print("No contacts found on this page. Ending scraping.")
                return False
        except Exception:
            # If 'no results' element is not found, continue processing the page.
            pass

        # Find the container(s) holding the contact articles.
        try:
            containers = self.driver.find_elements(By.CLASS_NAME, "dp-dfg-items")
        except Exception as e:
            print("Error finding contact containers:", e)
            return False

        # Loop through each container, and then through each article inside.
        for container in containers:
            articles: list[WebElement] = container.find_elements(By.TAG_NAME, "article")
            for article in articles:
                try:
                    # Extract the article title and its URL.
                    title_element: WebElement = article.find_element(
                        By.CSS_SELECTOR, "h3.entry-title a"
                    )
                    # Replace any en dash or em dash with a plain hyphen with spaces
                    title: str = re.sub(r"\s*[–—]\s*", " - ", title_element.text.strip())
                    article_url: str = title_element.get_attribute("href") or ""

                    # Extract the city/state information from the article.
                    city: str = article.find_element(
                        By.CLASS_NAME, "city-state"
                    ).text.strip() or ""

                    print(f"Name: {title} | URL: {article_url} | City: {city}")
                except Exception as e:
                    print("Error extracting article details:", e)
                    continue  # Skip to the next article if extraction fails

                # Add the contact if any of the fields contain data.
                if title or article_url or city:
                    self.contacts.append(
                        {
                            "Name": title,
                            "Url": article_url,
                            "Location": city,
                        }
                    )

        return True

    def save_contacts_to_csv(self) -> None:
        """
        Save the scraped contact details into a CSV file.

        This function writes the contact information to a CSV file with the specified fieldnames.
        """

        csv_dir = pathlib.Path("data")
        csv_dir.mkdir(parents=True, exist_ok=True)
        csv_file_path = csv_dir / "contacts_list.csv"

        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvFile:
            fieldnames: list[str] = ["Name", "Url", "Location"]
            writer: csv.DictWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.contacts)

    def get_company_pages(self, contact: dict) -> dict:
        """
        Retrieves unique company pages from the given list of contacts and returns them as a set.

        For each contact in the contact_list, this method calls `get_contact_details`
        to extract the associated company page URL. The results are stored in a set
        to automatically enforce uniqueness.

        :param companyList: A list of URLs from which to retrieve company pages.
        :return: A set of unique company page URLs.
        """

        link: str = self.get_company_url(contact["Url"])
        return {
            "Name": contact["Name"],
            "Link": link,
            "Location": contact["Location"],
            "Url": contact["Url"],
        }


#    def get_company_pages(self, companyList: list[str]) -> tuple[str, str]:
#        """
#        Retrieves unique company pages from the given list of contacts and returns them as a set.
#
#        For each contact in the contact_list, this method calls `get_contact_details`
#        to extract the associated company page URL. The results are stored in a set
#        to automatically enforce uniqueness.
#
#        :param companyList: A list of URLs from which to retrieve company pages.
#        :return: A set of unique company page URLs.
#        """
#        company_pages: set[str] = set()
#        for urlPage in companyList:
#            url: str = self.get_company_url(urlPage)
#            print(f"URL: {url} | Page: {urlPage}")
#            if url:
#                company_pages.add(url)
#        return company_pages

    def get_company_url(self, url: str) -> str:
        """
        Retrieves detailed contact information from a given URL.

        This method navigates to the specified URL, hides the cookie banner,
        and then extracts the contact details from the page.

        :param url: The URL of the contact page to scrape.
        :return: A dictionary containing the contact details.
        """
        self.driver.get(url)
        time.sleep(2)  # Allow page to load

        # Hide cookie banner if present.
        self.hide_cookie_banner()

        # Extract the contact details from the page.
        try:
            website: str = ""
            # Extract the contact details from the page.
            contact_details = self.driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[1]/div[3]/div[1]/div[3]/div/div[2]/div')
            if contact_details:
                # Extract the contact details from the page.
                website = contact_details.text.strip()
        except Exception as e:
            print("Error extracting contact details:", e)
            return ""

        return website

    def run(self):
        """
        Runs the scraper until 100 contacts are collected or there are no more pages.
        """
        try:
            while True:
                if not self.scrape_page():
                    break

                self.page += 1
                print(f"Collected {len(self.contacts)} contacts so far.")
                time.sleep(1)  # Pause before proceeding to the next page

        finally:
            self.driver_manager.quit()


if __name__ == "__main__":
    # Instantiate the ChromeDriverManager.
    driver_manager = ChromeDriverManager(headless=True)
    # Instantiate the scraper with the driver manager.
    scraper = ABATherapyScraper(driver_manager)
    scraper.run()
    scraper.save_contacts_to_csv()
    driver_manager.quit()
