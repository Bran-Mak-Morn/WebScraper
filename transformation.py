import pandas as pd
import re
import logging
from abstract_scraper import AbstractScraper


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_country_and_currency(url):
    """
    Add country and currency columns to the dataframe
    :param url: str
    :return: tuple of country and currency
    """
    # dictionary - country codes and currencies to match with the country names
    country_currency_map = {
        'uk': ('United Kingdom', 'GBP'),
        'cz': ('Czech Republic', 'CZK'),
        'de': ('Germany', 'EUR'),
        'fr': ('France', 'EUR'),
        'pl': ('Poland', 'PLN'),
    }

    # regex to find the country code in the URL
    try:
        match = re.search(r'notino\.co\.(?P<country_code>\w{2})', url)
        if match:
            country_code = match.group('country_code')
            if country_code in country_currency_map:
                return country_currency_map[country_code]
        logging.warning(f"No match found for country code in URL: {url}")
    except Exception as e:
        logging.error(f"Error processing URL: {e}")

    # return value if no match is found
    return 'Unknown', 'Unknown'


def transform_and_save_csv(url, input_file, output_file):
    """
    Transform the raw data to the final format and save it to the output file
    :param url: str
    :param input_file: str
    :param output_file: str
    :return: None
    """
    try:
        # matches country and currency from URL
        country, currency = add_country_and_currency(url)

        # read the scraped data
        df = pd.read_csv(input_file)

        # add new columns
        df['country'] = country
        df['currency'] = currency
        df['scraped_at'] = AbstractScraper.get_date()

        # save to new CSV file
        df.to_csv(output_file, index=False)
        logging.info(f"Data successfully transformed and saved to {output_file}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {input_file}, {e}")
    except pd.errors.EmptyDataError as e:
        logging.error(f"No data found in file: {input_file}, {e}")
    except Exception as e:
        logging.error(f"Error processing file {input_file}: {e}")
