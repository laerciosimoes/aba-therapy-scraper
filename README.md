# ABA Therapy Team Scraper 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Build: pytest](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/laerciosimoes/aba-therapy-scraper/actions)

A versatile Python scraper that automates the discovery of "Team" pages on ABA therapy provider websites, extracts member details (Name, Position, Location) using LLM-driven pipelines, and consolidates everything into a single CSV for easy analysis.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features ✨

- **Contact Discovery**: Load or generate a CSV of provider contacts (Name, URL, Location).
- **Page Discovery**: Identify each provider’s "Team" page URL.
- **LLM‑Driven Scraping**: Use `SmartScraperGraph` and `SmartScraperMultiGraph` (ScrapeGraphAI) for robust link and content extraction.
- **Interim Outputs**: Store raw JSON per site for inspection and reprocessing.
- **Consolidation**: Merge all member records into **`final_team_members.csv` — Consolidated results**.
- **Unit Testing**: Built‑in pytest suite for core extraction logic.

## Prerequisites 🛠

- **Python** 3.8+
- **Google Chrome** (for Selenium WebDriver)
- **ChromeDriver** matching your Chrome version
- **OpenAI API Key** (set in `.env`)

## Installation 🚀

1. **Clone the repo**:
   ```bash
   git clone https://github.com/laerciosimoes/aba-therapy-scraper.git
   cd aba-therapy-scraper
   ```
2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your environment**:
   ```bash
   cp .env.example .env
   # then edit .env to add your OPENAI_API_KEY
   ```

## Usage ▶️

1. Run the main script:
   ```bash
   python main.py
   ```
2. Check the `data/` folder for outputs:
   - `contacts_list.csv`      — Provider directory exports
   - `pages_list.csv`         — Detected "Team" page URLs
   - `team_members_<site>.json` — Raw JSON per site
   - **`final_team_members.csv` — Consolidated results**

## Project Structure 📂

```plaintext
├── main.py                     # Entry point with full workflow
├── scrapper/
│   ├── driverManager.py        # Selenium ChromeDriver manager
│   ├── ABATherapyScraper.py    # Discovers team page URLs
│   └── TeamExtractor.py        # LLM‑powered extraction logic
├── data/                       # Input (contacts) & outputs (pages, JSON, CSV)
├── tests/
│   └── test_team_extractor.py  # pytest suite for TeamExtractor
├── requirements.txt            # Python dependencies
├── .env.example                # Sample env file for API keys
└── LICENSE                     # MIT License text
```

## Testing ✅

Execute the pytest suite:
```bash
pytest tests/
```

## Roadmap 🛣

- 🔄 **Complete Coverage**: Loop through all 50 states (filter by state) to exhaustively capture providers.
- ⚙️ **Optimize Scraping**: Integrate more Selenium fallbacks to reduce LLM token usage and costs.
- 🌐 **Language Enforcement**: Force English extraction to avoid inconsistencies from non‑English pages.
- 💡 **Retry Logic**: Add automated retries and backoff for transient failures.
- 📊 **Analytics Dashboard**: Provide a summary report or visual dashboard of extracted data.

## Contributing 🤝

1. Fork the repo & create a branch: `git checkout -b feature/my-feature`
2. Commit your changes: `git commit -m "Add my feature"`
3. Push: `git push origin feature/my-feature`
4. Open a Pull Request.

Please follow the [code of conduct](CODE_OF_CONDUCT.md).

## License 📜

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

