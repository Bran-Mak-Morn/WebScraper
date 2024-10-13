# WebScraper
A Python project for scraping website data using Selenium, and transforming it into a CSV format.

## Overview

Bot scrapes data from "notino.co.uk" and transforms it into a CSV format.

### Technologies
Python & Selenium for backend logic.


### Licence
This project is under MIT license. Libraries and modules have their own licenses:
- Selenium: Apache License 2.0
- Python: Python Software Foundation License

## Files

- `abstract_scraper.py`: Base class with scraping methods.
- `scraper.py`: Scrapes data from Notino and saves to `notino_raw.csv`.
- `transformation.py`: Transforms raw data, adds extra columns, and saves to `notino_transformed.csv`.

## Setup

### Prerequisites

- Python 3.7+
- Google Chrome & ChromeDriver
- Required Python packages

### Installation

1. Install packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the URL in `scraper.py` to the Notino website for the region you want to scrape (e.g., https://www.notino.co.uk/toothpaste/).

2. Run the scraper to collect raw data:
    ```sh
    python scraper.py
    ```

3. The raw data will be saved to `notino_raw.csv`.

4. Transform the raw data to the final format:
    ```sh
    python transformation.py
    ```

5. The transformed data will be saved to `notino_transformed.csv`.
   
## Project Highlights

- **Web Scraping**: Demonstrates how to scrape data from dynamically loaded web pages using Selenium.
- **Data Transformation**: Shows how to transform and enhance scraped data with additional information and save it in a structured format.
- **Error Handling and Logging**: Incorporates robust error handling and logging for better debugging and maintenance.
