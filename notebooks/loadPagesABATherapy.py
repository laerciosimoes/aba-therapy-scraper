import csv
from scrapper.driverManager import ChromeDriverManager
from scrapper.ABATherapyScraper import ABATherapyScraper
import pathlib


def load_contact_list() -> list[str]:
    with open("data/contacts_list.csv", "r", encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        return [row[1] for row in reader]

def main() -> None:
    # Instantiate the ChromeDriverManager.
    driver_manager = ChromeDriverManager(headless=True)
    # Instantiate the scraper with the driver manager.
    scraper = ABATherapyScraper(driver_manager)

    contact_list = load_contact_list()
    urlPages: set[str] = scraper.get_company_pages(contact_list[1:])

    csv_dir = pathlib.Path("data")
    csv_dir.mkdir(parents=True, exist_ok=True)
    csv_file_path = csv_dir / "pages_list.csv"

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvFile:
        fieldnames: list[str] = ["Url"]
        writer: csv.DictWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([ {"Url": url} for url in urlPages])

    print(f"Total unique company pages: {len(urlPages)}")

    driver_manager.quit()

if __name__ == "__main__":
    main()
