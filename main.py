import random
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


path = "C:/chromedriver.exe"
s = Service(executable_path=path)
driver = webdriver.Chrome(service=s)


def get_data():
    driver.get('https://online.metro-cc.ru/category/sladosti-chipsy-sneki/chipsy-suhari-sneki')
    time.sleep(9)
    try:
        driver.find_element(By.CLASS_NAME, 'shop-select-dialog__container').click()
    except Exception as e:
        print(e)
    try:
        for el in driver.find_elements(By.CLASS_NAME, "product-card__content"):
            print(el.find_element(By.CLASS_NAME, "product-price__sum-rubles").text)
    except Exception as e:
        print(e)


def main():
    get_data()


if __name__ == "__main__":
    main()
