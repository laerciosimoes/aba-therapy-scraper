# ABA Therapy Team Scraper

A Python-based web scraper that automates the extraction of team member information from ABA therapy provider websites. It discovers "Team" pages for each provider, extracts member details (name, position, location), and consolidates the data into a final CSV.

## Features

- **Contact Discovery**: Loads or generates a list of provider contacts (Name, URL, Location).
- **Page Discovery**: Finds "Team" pages on each provider's site.
- **Data Extraction**: Utilizes `SmartScraperGraph` and `SmartScraperMultiGraph` to extract team member details via LLM-driven pipelines.
- **Interim Storage**: Saves raw JSON outputs per page for inspection.
- **Consolidation**: Merges all extracted members into a single `final_team_members.csv`.
- **Unit Testing**: Provides pytest suite for core extraction logic.

## Prerequisites

- Python 3.8 or higher
- [Google Chrome](https://www.google.com/chrome/) (for Selenium)
- A valid OpenAI API key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/aba-therapy-scraper.git
   cd aba-therapy-scraper
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # macOS/Linux
   .\.venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your OpenAI API key:
   ```ini
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Ensure you have (or allow generation of) `data/contacts_list.csv`.
2. Run the main script:
   ```bash
   python scraper_script_with_docs.py
   ```
3. Outputs will be saved to `data/`:
   - `pages_list.csv` &mdash; Discovered team page URLs
   - `team_members_<site>*.json` &mdash; Raw JSON per site
   - `final_team_members.csv` &mdash; Consolidated results

## Project Structure

```
├── scraper_script_with_docs.py   # Main orchestrator script with docs
├── scrapper/
│   ├── driverManager.py         # ChromeDriverManager for Selenium
│   ├── ABATherapyScraper.py      # Logic to discover team page URLs
│   └── TeamExtractor.py          # LLM-driven extraction logic
├── data/                         # Input/output directory (CSV/JSON)
├── notebooks/                    # Intermediate codes for testing and researching
├── tests/
│   └── test_team_extractor.py    # Pytest suite for TeamExtractor
├── requirements.txt              # Python dependencies
└── .env.example                  # Example environment file
```

## Testing

Run the pytest suite:
```bash
pytest tests/
```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m 'Add my feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

