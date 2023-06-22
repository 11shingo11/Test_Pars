import random
import time
import re
import openpyxl
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


path = "C:/chromedriver.exe"
s = Service(executable_path=path)
driver = webdriver.Chrome(service=s)

workbook = openpyxl.Workbook()
worksheet = workbook.active
# добавляем колонки в таблицу
worksheet['A1'] = 'id'
worksheet['B1'] = 'наименование'
worksheet['C1'] = 'ссылка на товар'
worksheet['D1'] = 'регулярная цена'
worksheet['E1'] = 'промо цена'
worksheet['F1'] = 'бренд'

def contains_latin_letters(text):
    pattern = r'[a-zA-Z]'
    return re.search(pattern, text) is not None


def get_data():
    row = 2
    page = 1
    while page != 11:
        driver.get(f'https://online.metro-cc.ru/category/sladosti-chipsy-sneki/chipsy-suhari-sneki?page={page}')
        time.sleep(1)
        try:
            driver.find_element(By.CLASS_NAME, 'shop-select-dialog__container').click()
        except Exception as e:
            print(e)
        try:
            for el in driver.find_elements(By.CLASS_NAME, "product-card__content"):
                id = el.find_element(By.XPATH, '..').get_attribute("data-sku")
                worksheet['A' + str(row)] = id
                title = el.find_element(By.CSS_SELECTOR, '[data-qa = "product-card-photo-link"]').get_attribute("title")
                worksheet['B' + str(row)] = title
                for i in [title.split(" ")]:
                    for brand in i:
                        text = brand
                        if contains_latin_letters(text):
                            if len(brand) > 1:
                                worksheet['F' + str(row)] = brand+"\n"
                link = el.find_element(By.CSS_SELECTOR, '[data-qa = "product-card-photo-link"]').get_attribute("href")
                worksheet['C' + str(row)] = link
                try:
                    i=1
                    for elm in el.find_elements(By.CLASS_NAME, "product-price__sum"):
                        try:
                            try:
                                rub = elm.find_element(By.CLASS_NAME, "product-price__sum-rubles")
                                penc = elm.find_element(By.CLASS_NAME, "product-price__sum-penny")
                                if i == 1:
                                    worksheet['D' + str(row)] = rub.text + penc.text
                                    i += 1
                                else:
                                    worksheet['E' + str(row)] = rub.text + penc.text
                            except:
                                rub = elm.find_element(By.CLASS_NAME, "product-price__sum-rubles")
                                if i == 1:
                                    worksheet['D' + str(row)] = rub.text
                                    i+=1
                                else:
                                    worksheet['E' + str(row)] = rub.text

                        except:
                            rub = elm.find_element(By.CLASS_NAME, "product-price__sum-rubles")
                            worksheet['D' + str(row)] = rub.text
                        #workbook.save('products123test.xlsx')
                except:
                    pass
                row += 1
        except:
            pass
        page += 1


        # saving table
    workbook.save('products123test.xlsx')
    driver.close()
    driver.quit()


def main():
    get_data()


if __name__ == "__main__":
    main()
