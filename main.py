#!/usr/bin/env python3
"""
scraper_script_with_docs.py

This script orchestrates the extraction of team member information from ABA therapy provider websites.

Workflow:
 1. Load or generate a list of provider contacts (Name, URL, Location).
 2. Discover company "team" pages for each provider.
 3. Extract team member details (Name, Position, Location) from each team page.
 4. Consolidate all team members into a final CSV output.

Dependencies:
  - selenium
  - tqdm
  - scrapper.driverManager.ChromeDriverManager
  - scrapper.ABATherapyScraper.ABATherapyScraper
  - scrapper.TeamExtractor.TeamExtractor

Usage:
  Ensure you have a `data/contacts_list.csv` file or allow the scraper to generate it.
  Run the script:
      python scraper_script_with_docs.py

Outputs:
  - data/pages_list.csv         : Discovered team page URLs.
  - data/team_members_*.json    : Raw JSON files per page.
  - data/final_team_members.csv : Consolidated team member info.
"""

import csv
import json
import pathlib

from tqdm import tqdm

from scrapper.driverManager import ChromeDriverManager
from scrapper.ABATherapyScraper import ABATherapyScraper
from scrapper.TeamExtractor import TeamExtractor


def load_contacts_from_csv(
    csv_path: pathlib.Path = pathlib.Path("data/contacts_list.csv"),
) -> list[dict]:
    """
    Load provider contacts from a CSV file.

    Each row must contain: Name, URL, Location.

    Args:
        csv_path (pathlib.Path): Path to the contacts CSV file.

    Returns:
        List[dict]: A list of contact dictionaries with keys 'Name', 'Url', and 'Location'.

    Raises:
        FileNotFoundError: If the CSV file does not exist at csv_path.
    """
    contacts: list[dict] = []
    if not csv_path.exists():
        raise FileNotFoundError(f"Contacts file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Expecting exactly three columns per row
            name, url, location = row
            contacts.append(
                {"Name": name.strip(), "Url": url.strip(), "Location": location.strip()}
            )
    return contacts


def main() -> None:
    """
    Main entry point for team member scraping workflow.

    Workflow steps:
      1. Initialize Selenium WebDriver (headless by default).
      2. Load or generate contacts list.
      3. Discover "team" page URLs for each contact.
      4. Extract team member data and save interim JSON files.
      5. Consolidate extracted data into a final CSV.

    Side effects:
      - Creates/reads `data/pages_list.csv` and `data/team_members_*.json`.
      - Writes `data/final_team_members.csv` with columns: Url, Name, Title, Company, Location.
    """
    # Ensure data directory exists
    data_dir = pathlib.Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Initialize browser driver (headless)
    driver_manager = ChromeDriverManager(headless=True)
    scraper = ABATherapyScraper(driver_manager)
    team_extractor = TeamExtractor()

    # Step 1: Load or generate contacts_list.csv
    contacts_csv = data_dir / "contacts_list.csv"
    try:
        scraper.contacts = load_contacts_from_csv(contacts_csv)
    except FileNotFoundError:
        scraper.run()
        scraper.save_contacts_to_csv(str(contacts_csv))
        scraper.contacts = load_contacts_from_csv(contacts_csv)

    # Step 2: Discover or load team page URLs
    pages_csv = data_dir / "pages_list.csv"
    url_pages: list[dict] = []
    if pages_csv.exists():
        with pages_csv.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                url_pages.append(row)
    else:
        for contact in tqdm(scraper.contacts, desc="Finding pages", unit="contact"):
            page_info = scraper.get_company_pages(contact)
            url_pages.append(page_info)
        # Persist page list
        with pages_csv.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=["Name", "Link", "Location", "Url"]
            )
            writer.writeheader()
            for page in url_pages:
                writer.writerow(page)

    # Step 3: Extract team members per page
    for page in tqdm(url_pages, desc="Extracting team members", unit="page"):
        # Build a safe filename for JSON output
        safe_link = page["Link"].replace("/", "_").replace(".", "_")
        json_path = data_dir / f"team_members_{safe_link}.json"
        if not json_path.exists():
            members = team_extractor.extract(page["Link"])
            with json_path.open("w", encoding="utf-8") as jf:
                json.dump(members, jf, indent=4)

    # Quit Selenium driver to free resources
    driver_manager.quit()

    # Step 4: Consolidate all team members into final CSV
    all_members: list[dict] = []
    for json_file in data_dir.glob("team_members_*.json"):
        with json_file.open("r", encoding="utf-8") as jf:
            all_members.extend(json.load(jf))

    final_csv = data_dir / "final_team_members.csv"
    with final_csv.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Url", "Name", "Title", "Company", "Location"])
        for member in tqdm(all_members, desc="Saving team members", unit="member"):
            # Map member URL back to company
            page = next((p for p in url_pages if p["Link"] == member.get("Url")), {})
            writer.writerow(
                [
                    member.get("Url", ""),
                    member.get("name", ""),
                    member.get("position", ""),
                    page.get("Name", ""),
                    page.get("Location", ""),
                ]
            )


if __name__ == "__main__":
    main()
