# 📱 eBay Flagship Phone Scraper & Cleaner

This project is a complete pipeline for **scraping**, **storing**, and **cleaning** pricing data of flagship iPhones from eBay. 

The scraper was initially written manually and later optimized with AI to behave more like a human and reduce the risk of detection.

---

## 🚀 Features

### 🕵️ Human-like Stealth Web Scraper
- Scraper mimics human browsing behavior using:
  - `curl_cffi` for lightweight requests
  - `nodriver` as a fallback headless browser
  - Randomized user agents with `fake_useragent`
  - Random delays, scrolling, and page loads
- Searches for various phone models across different item conditions and pages

### 🗃️ PostgreSQL Integration
- Data is saved directly into a local PostgreSQL database using a custom function `add_a_record()`
- This ensures structured and consistent storage before any processing

### 🧹 Data Cleaning
- Exported raw data (`products.csv`) is cleaned and transformed into `clean_phones.csv`
- Cleaning steps include:
  - Extracting model names from messy eBay titles using regex
  - Standardizing prices, shipping, and location data
  - Fixing inconsistent formatting and removing irrelevant records

---

## 📁 Project Structure
📦 Ebay_FLAGSHIP_Project/<br>
├── .venv/ # Virtual environment (excluded via .gitignore)<br>
├── pycache/ # Python cache files<br>
├── .ipynb_checkpoints/ # Jupyter auto-saves<br>
├── latest_logs/ # Optional logging<br>
├── cleaning_scrapped_data.ipynb # Notebook for data cleaning<br>
├── clean_phones.csv # Final cleaned dataset<br>
├── products.csv # Raw scraped dataset from PostgreSQL<br>
├── database.py # PostgreSQL setup and insert logic<br>
├── test_webscrapper_for_Ebay.py # Initial or testing scraper<br>
├── libraries_requirment.txt # Required dependencies<br>
├── .gitignore<br>
├── README.md<br>


---

## 📊 Data Analysis

🚧 **Data analysis is in progress** — but you are welcome to explore `clean_phones.csv` and draw your own insights! The data is cleaned, structured, and ready for use.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r libraries_requirment.txt

