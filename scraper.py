from abstract_scraper import AbstractScraper
from transformation import transform_and_save_csv, add_country_and_currency
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_element_text(element, by, value, default="NA"):
    """
    Helper function to get the text of a web element
    :param element: WebElement to search within
    :param by: Method to locate elements
    :param value: The locator value to be used with the 'by' parameter
    :param default: The value to return if the element is not found (default is "NA")
    :return: The text value of the element, or the default value if not found
    """
    try:
        return element.find_element(by, value).text
    except:
        return default


def get_element_attribute(element, by, value, attribute, default="NA"):
    """
    Helper function to get the attribute of a web element
    :param element: WebElement to search within
    :param by: Method to locate elements
    :param value: The locator value to be used with the 'by' parameter
    :param attribute: The attribute name to retrieve from the found sub-element
    :param default: The value to return if the sub-element or attribute is not found (default is "NA")
    :return: The attribute value as a string, or the default value if not found
    """
    try:
        return element.find_element(by, value).get_attribute(attribute)
    except:
        return default


# get url, AbstractScraper instance
url = "https://www.notino.co.uk/toothpaste/"
test = AbstractScraper()
test.get_url(url)

# wait for a page to load
try:
    WebDriverWait(test.driver, 20).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="product-container"]'))
    )
except Exception as e:
    logging.error(f"Error waiting for page to load: {e}")

# all product containers
all_product_containers = test.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-container"]')

# excluding PROMO banners
product_containers = [container for container in all_product_containers
                      if container.get_attribute("data-recommendation") != "promo-banner"]

# check - total number of containers, excluding promo banners
logging.info(f"Total number of all product containers: {len(all_product_containers)}")
logging.info(f"Total number of products: {len(product_containers)}")


for product_number, product_container in enumerate(product_containers, start=1):
    # Extract data
    name = get_element_text(product_container, By.TAG_NAME, "h3")
    brand = get_element_text(product_container, By.TAG_NAME, "h2")
    price = get_element_text(product_container, By.CSS_SELECTOR, 'span[data-testid="price-component"]')
    link = get_element_attribute(product_container, By.CSS_SELECTOR, 'a', "href")
    image = get_element_attribute(product_container, By.CSS_SELECTOR, 'img', "src")
    discount = get_element_text(product_container, By.CSS_SELECTOR, 'span.styled__DiscountValue-sc-1b3ggfp-1.jWXmOz',
                                default="0")

    logging.info(f"Number {product_number}, name: {name}")
    logging.info(f"Number {product_number}, brand: {brand}")
    logging.info(f"Number {product_number}, price: {price}")
    logging.info(f"Number {product_number}, link: {link}")
    logging.info(f"Number {product_number}, image: {image}")
    logging.info(f"Number {product_number}, discount: {discount}")

    # save data
    test.save_data(name, brand, price, link, image, discount)

# end session, data exported to csv
test.end_session()
test.export_data_to_csv("notino_raw.csv")

# add country and currency
add_country_and_currency(url)
transform_and_save_csv(url, "notino_raw.csv", "notino_transformed.csv")
