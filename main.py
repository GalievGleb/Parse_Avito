import json

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver = uc.Chrome()
driver.get(
    'https://www.avito.ru/kazan/bytovaya_elektronika?cd=1&q=%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE')


class AvitoParse:
    def __init__(self, url: str, items: list, count: int = 100, version_main=None):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='paginator-button/next']") and self.count > 0:
            self.__parse_page()
            self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='paginator-button/next']").click()
            self.count -= 1

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in titles:
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            description = title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            data = {
                'name': name,
                'description': description,
                'url': url,
                'price': price
            }
            if any([item.lover() in description.lower() for item in self.items]) and int(price)==0:
                self.data.append(data)
                print(name, description, url, price)
        self.__save_data()

    def __save_data(self):
        with open("item.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()


if __name__ == "__main__":
    AvitoParse(
        url='https://www.avito.ru/kazan/bytovaya_elektronika?cd=1&q=%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE',
        count=1,
        version_main=108,
        items=["телевизор", "пульт"]
        ).parse()
