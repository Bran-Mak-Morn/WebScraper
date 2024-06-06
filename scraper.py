from abstract_scraper import AbstractScraper
from transformation import transform_and_save_csv, add_country_and_currency
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Constants
URL = "https://www.notino.co.uk/toothpaste/"
WAIT_TIMEOUT = 20
PRODUCT_CONTAINER_SELECTOR = 'div[data-testid="product-container"]'
PRICE_COMPONENT_SELECTOR = 'span[data-testid="price-component"]'
DISCOUNT_SELECTOR = 'span.styled__DiscountValue-sc-1b3ggfp-1.jWXmOz'


def get_element_text(element, by, value, default="NA"):
    """
    Gets the text from the web element
    :param element: web element
    :param by: By object
    :param value: tag name or CSS selector
    :param default:
    :return: text of the element
    """
    try:
        return element.find_element(by, value).text
    except:
        return default


def get_element_attribute(element, by, value, attribute, default="NA"):
    """
    Gets the attribute from the web element
   :param element: web element
    :param by: By object
    :param value: tag name or CSS selector
    :param attribute: attribute name
    :param default:
    :return: attribute of the element
    """
    try:
        return element.find_element(by, value).get_attribute(attribute)
    except:
        return default


def extract_product_data(product_container):
    """
    Extracts the product data from the product container
    :param product_container:
    :return: dictionary of product data
    """
    name = get_element_text(product_container, By.TAG_NAME, "h3")
    brand = get_element_text(product_container, By.TAG_NAME, "h2")
    price = get_element_text(product_container, By.CSS_SELECTOR, PRICE_COMPONENT_SELECTOR)
    link = get_element_attribute(product_container, By.CSS_SELECTOR, 'a', "href")
    image = get_element_attribute(product_container, By.CSS_SELECTOR, 'img', "src")
    discount = get_element_text(product_container, By.CSS_SELECTOR, DISCOUNT_SELECTOR, default="0")
    return {
        'name': name,
        'brand': brand,
        'price': price,
        'link': link,
        'image': image,
        'discount': discount
    }


def my_scraper(url):
    """
    Scrapes the given URL
    :param url:
    :return: None
    """
    scraper = AbstractScraper()
    scraper.get_url(url)

    # Wait for the page to load
    try:
        WebDriverWait(scraper.driver, WAIT_TIMEOUT).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, PRODUCT_CONTAINER_SELECTOR))
        )
    except Exception as e:
        logging.error(f"Error waiting for page to load: {e}")

    all_product_containers = scraper.driver.find_elements(By.CSS_SELECTOR, PRODUCT_CONTAINER_SELECTOR)
    product_containers = [container for container in all_product_containers
                          if container.get_attribute("data-recommendation") != "promo-banner"]

    logging.info(f"Total number of all product containers: {len(all_product_containers)}")
    logging.info(f"Total number of products: {len(product_containers)}")

    for product_number, product_container in enumerate(product_containers, start=1):
        product_data = extract_product_data(product_container)
        logging.info(f"Product {product_number}: {product_data}")
        scraper.save_data(**product_data)

    scraper.end_session()
    scraper.export_data_to_csv("notino_raw.csv")

    add_country_and_currency(url)
    transform_and_save_csv(url, "notino_raw.csv", "notino_transformed.csv")


if __name__ == "__main__":
    my_scraper(URL)