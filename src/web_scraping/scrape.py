import os
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(
    filename="scrape_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# driver_path = "C:\Users\AzeezAdebolaOgundeko\Downloads\neonX\src\web_scraping\chromedriver.exe"
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome()


class ScrapeAmazon:
    def __init__(self) -> None:
        self.url = "https://www.amazon.com/"
        self.index = []
        self.product_asin = []
        self.product_uuid = []
        self.product_name = []
        self.product_price = []
        self.product_ratings = []
        self.product_ratings_num = []
        self.product_link = []
        self.img_url = []
        self.img_alt = []

        # self.product_brand = []
        # self.pro_category = []

    def _search_product_list(self, product_name):
        # search_path = os.path.join(URL)

        # getting the url
        driver.get(self.url)
        driver.implicitly_wait(5)

        search = driver.find_element(By.ID, "twotabsearchtextbox")

        # to enter the keyword
        search.send_keys(product_name)

        # to submit the value o
        submit_value = driver.find_element(By.ID, "nav-search-submit-button")
        submit_value.click()

        driver.implicitly_wait(5)

    def _search_product_detail(self, product_name):
        search_product = ScrapeAmazon()
        search_product._search_product_list(product_name)

    def get_products_attributes(self, product_name):
        search_product = ScrapeAmazon()
        search_product._search_product_list(product_name)

        if not search_product:
            driver.quit()

        # to start scraping the list of items
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')
            )
        )
        # getting the product name, asin
        for item in items:
            # scrape product index
            index = item.get_attribute("index")
            self.index.append(index)
            # scrape product name
            name = item.find_element(
                By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]'
            )
            self.product_name.append(name.text)

            # scrape product asin number
            prod_asin = item.get_attribute("data-asin")
            self.product_asin.append(prod_asin)

            # scrape product uuid
            prod_uuid = item.get_attribute("data-uuid")
            self.product_uuid.append(prod_uuid)

            # scrape price
            whole_price = item.find_elements(
                By.XPATH, './/span[@class = "a-price-whole"]'
            )
            fraction_price = item.find_elements(
                By.XPATH, './/span[@class = "a-price-fraction"]'
            )

            if whole_price != [] and fraction_price != []:
                price = ".".join([whole_price[0].text, fraction_price[0].text])
            else:
                price = 0

            self.product_price.append(price)

            # scrape product ratings and rating numbers
            ratings_box = item.find_elements(
                By.XPATH, './/div[@class = "a-row a-size-small"]/span'
            )

            if ratings_box != []:
                ratings = ratings_box[0].get_attribute("aria-label")
                ratings_num = ratings_box[1].get_attribute("aria-label")
            else:
                ratings, ratings_box = 0, 0

            self.product_ratings.append(ratings)
            self.product_ratings_num.append(ratings_num)

            # scrape product details link
            link = item.find_element(
                By.XPATH,
                './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]',
            ).get_attribute("href")
            self.product_link.append(link)

            # scrape img url and alt_text
            img_url = item.find_element()


        driver.quit()

        response = {
            "index": self.index,
            "product uuid": self.product_uuid,
            "product name": self.product_name,
            "product asin": self.product_asin,
            "product price": self.product_price,
            "product rating": self.product_ratings,
            "product ratings number": self.product_ratings_num,
            "product link": self.product_link,
            "image alt": self.img_alt,
            "image url": self.img_url,
        }

        logging.info(f"""{response}""")
        # print(response)
        return response


scraper = ScrapeAmazon()
scraper.get_products_attributes("computers")
print(scraper)
