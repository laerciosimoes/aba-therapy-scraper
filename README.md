# ABA Therapy Team Scraper 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Build: pytest](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/laerciosimoes/aba-therapy-scraper/actions)

A powerful, LLM-driven Python scraper designed to automate the discovery of "Team" pages from ABA therapy provider websites. It extracts key team member information—**Name**, **Position**, and **Location**—and compiles everything into a structured CSV for easy analysis.

---

## 📚 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Enriched Data](#enriched-data)
- [License](#license)

---

## ✨ Features

- 🔍 **Contact Discovery**: Load or generate a CSV containing provider Name, Website, and Location.
- 🌐 **Page Discovery**: Automatically identify and validate the “Team” or “About Us” pages.
- 🧠 **LLM-Powered Extraction**: Uses `SmartScraperGraph` and `SmartScraperMultiGraph` (ScrapeGraphAI) to extract structured team member details.
- 💾 **Intermediate Outputs**: Stores JSON snapshots of raw team member data per provider.
- 📦 **Final Consolidation**: Merges extracted records into a single `final_team_members.csv` file.
- ✅ **Built-in Testing**: Pytest suite available to validate core extraction logic.

---

## 🛠 Prerequisites

- **Python** 3.8 or newer  
- **Google Chrome** (for Selenium)  
- **ChromeDriver** matching your Chrome version  
- **OpenAI API Key** (configured in `.env`)

---

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/laerciosimoes/aba-therapy-scraper.git
   cd aba-therapy-scraper
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .\.venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

---

## ▶️ Usage

1. Run the scraper:
   ```bash
   python main.py
   ```

2. Check the `data/` folder for generated files:
   - `contacts_list.csv` — Source list of ABA therapy providers
   - `pages_list.csv` — Discovered "Team" page URLs
   - `team_members_<site>.json` — Raw extracted member data
   - `final_team_members.csv` — ✅ Fully consolidated results

---

## 📂 Project Structure

```plaintext
├── main.py                            # Main entry script
├── scrapper/
│   ├── driverManager.py               # Selenium ChromeDriver manager
│   ├── ABATherapyScraper.py           # Discovers "Team" pages
│   └── TeamExtractor.py               # Handles LLM-based content parsing
├── data/                              # Input & output files
├── tests/
│   ├── test_driverManager.py          # Test Selenium ChromeDriver manager
│   ├── test_ABATherapyScraper.py      # Test Discovers "Team" pages
│   └── test_TeamExtractor.py          # test Handles LLM-based content parsing
├── requirements.txt                   # Python dependencies
├── .env.example                       # Sample environment config
└── LICENSE                            # MIT License
```

---

## ✅ Testing

To run the test suite:

```bash
pytest tests/
```

---

## 🛣 Roadmap

- 🔄 **Full Coverage**: Scrape providers in all 50 states with location filters.
- ⚙️ **Efficiency Improvements**: Introduce more Selenium fallbacks to reduce LLM costs.
- 🌐 **Language Standardization**: Force English for consistent parsing.
- 🔁 **Retry & Backoff**: Add auto-retry logic for flaky or timeout-prone pages.
- 📊 **Analytics Dashboard**: Build a lightweight visual dashboard to explore the extracted data.

---

## 🤝 Contributing

1. Fork the repo and create a new feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```
2. Commit your changes:
   ```bash
   git commit -m "Add my feature"
   ```
3. Push your branch:
   ```bash
   git push origin feature/my-feature
   ```
4. Submit a Pull Request!

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📈 Enriched Data Notes

- Using **Clay** with free credits to enrich contact information, including **Work Email** and **Company Details**.
- Currently need ~1,800 credits to unlock **Mobile Numbers** (requires LinkedIn profile URL).
- LinkedIn enrichment is gated behind **Personal Email**, which is typically obtained via a **Facebook profile** (not currently viable due to credit limitations).

### Sheets Created:
- [ABA Therapy - 150 (150 enriched records)](https://docs.google.com/spreadsheets/d/1G_xMpMKMVcdz8jLJ3znFEMrXgvWhQKSPhvS03Qsc5_U/edit?usp=sharing)
- [ABA Therapy (841 enriched records)](https://docs.google.com/spreadsheets/d/17_7jOArjskLWYYYBW8IlAAy-yVEqE7zXGc4P_M_4vMs/edit?usp=sharing)

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.