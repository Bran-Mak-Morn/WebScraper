from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import datetime
import csv
import requests
import logging


class AbstractScraper:
    """
    Base class for scrapers.
    """
    def __init__(self):
        """
        Initialize the scraper
        """
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except WebDriverException as e:
            logging.error(f"Error initializing the WebDriver: {e}")
        self.data = []

    def get_url(self, url: str):
        """
        Get the given URL
        :param url: string
        :return: True if the request was successful, False otherwise
        """
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logging.error(f"Error navigating to {url} with Selenium: {e}")
            return False

    def post_url(self, url: str, data: dict):
        """
        Send POST request to the given URL with the given data
        :param url:
        :param data:
        :return: response text
        """
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error sending POST request to {url}: {e}")
            return None

    def end_session(self):
        """
        End the Selenium session
        :return: None
        """
        self.driver.quit()

    def save_data(self, name, brand, price, link, image, discount):
        """
        Add scraped data to the data list
        :param name:
        :param brand:
        :param price:
        :param link:
        :param image:
        :param discount:
        :return: None
        """
        self.data.append({
            'name': name,
            'brand': brand,
            'price': price,
            'link': link,
            'image': image,
            'discount': discount
        })

    def export_data_to_csv(self, filename):
        """
        Dump data to CSV file
        :param filename:
        :return: None
        """
        if self.data:
            keys = self.data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.data)
        else:
            logging.warning("No data to export to CSV.")

    @staticmethod
    def get_date():
        """
        Get current date and time in format YYYY-MM-DD HH:MM:SS
        :return: str
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
