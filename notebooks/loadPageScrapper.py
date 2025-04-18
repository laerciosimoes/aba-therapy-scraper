import csv
from scrapper.PageScrapper import PageScrapper
import pathlib
from scrapper.TeamExtractor import TeamExtractor
from tqdm import tqdm

def load_page_list() -> list[str]:
    with open("data/pages_list.csv", "r", encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        return [row[0] for row in reader]

def check_has_team_page(scrapper: PageScrapper, site: str) -> bool:
    result: bool = scrapper.has_team_page(site)
    return result

def scrape_team_members(scrapper: PageScrapper, site: str) -> list[dict]:
    team: list[dict] = scrapper.scrape_company_team(site)
    return team
def save_team_members(team_members: list[dict]) -> None:
    print("Saving team members")
    csv_dir = pathlib.Path("data")
    csv_dir.mkdir(parents=True, exist_ok=True)
    csv_file_path = csv_dir / "team_members_list.csv"

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvFile:
        fieldnames: list[str] = ["url", "name", "position"]
        writer: csv.DictWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        # team_members is now a flat list of dicts, each already containing 'url'
        for member in team_members:
            writer.writerow(member)

def main() -> None:

    sites = load_page_list()

    # for testing you can override:
    # sites = ["Url", "https://www.abskids.com", "https://abaenhancement.com"]

    all_members: list[dict] = []

    extractor = TeamExtractor()
    for site in tqdm(sites[1:], desc="Scraping team members", unit="site"):
        # use tqdm.write so the print doesn’t break the progress bar
        tqdm.write(f"Scraping team members for {site}")
        members = extractor.extract(site)
        # annotate each member with its source url and adapt 'title'→'position' if needed
        for m in members:
            all_members.append({
                "url": site,
                "name": m["name"],
                # if your extractor returns 'title', rename here:
                "position": m.get("position", m.get("title", "")),
        })

    save_team_members(all_members)


if __name__ == "__main__":
    main()
