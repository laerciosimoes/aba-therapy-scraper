from scrapper.driverManager import ChromeDriverManager
from scrapper.ABATherapyScraper import ABATherapyScraper

def main():
    # Instantiate the ChromeDriverManager.
    driver_manager = ChromeDriverManager(headless=True)
    # Instantiate the scraper with the driver manager.
    scraper = ABATherapyScraper(driver_manager)
    scraper.run()
    scraper.save_contacts_to_csv()


if __name__ == "__main__":
    main()
