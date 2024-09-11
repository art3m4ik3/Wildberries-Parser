from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv

articles: list[int] = []  # нужно заполнить нужными артиклами

options = Options()
options.add_argument("--incognito")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def parse(article: int):
    link = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"

    driver = webdriver.Chrome(options=options)
    driver.set_window_position(9999999, 99999999)
    driver.get(link)

    try:
        price = (
            WebDriverWait(driver, 5)
            .until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "span.price-block__wallet-price")
                )
            )
            .text
        )
    except (NoSuchElementException, TimeoutException):
        price = (
            WebDriverWait(driver, 5)
            .until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "ins.price-block__final-price")
                )
            )
            .text
        )

    if price:
        print(f"{article}: {price}")
        write_data(article, price)

    driver.quit()


def write_data(article: int, price: int):
    with open("data.csv", "a", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["article", "price"])
        writer.writerow({"article": article, "price": price})


def init_csv():
    with open("data.csv", "w", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["article", "price"])
        writer.writeheader()


if __name__ == "__main__":
    init_csv()

    for article in articles:
        parse(article)
