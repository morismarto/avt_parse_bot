from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from typing import List, LiteralString
from time import sleep
from src.city_list import cities, ex
import pyshorteners


class Parser:
    city: str = 'Москва'
    def __init__(self, query: str) -> None:
        self.__query: str = query
        self.__URL = 'https://www.avito.ru/'
        self.__chrome = webdriver.Chrome
        self.__chrome_opt = webdriver.ChromeOptions()
        self.__cities: dict[str, str] = cities
        self.__result = []
        self.ex = ex

    def __name_filter(self, name) -> None | bool:
        for i in self.ex:
            if i in name:
                return False
        return True    

    # def __get_str_result(self) -> LiteralString:
    #     return ''.join(self.__result)

    def __shorten_url(self, url):
        return pyshorteners.Shortener().clckru.short(url)

    def __set_stealth_opt(self) -> None:
        self.__chrome_opt.add_argument("--headless=new")
        self.__chrome_opt.add_argument("start-maximized")
        self.__chrome_opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__chrome_opt.add_experimental_option('useAutomationExtension', False)

    def __set_stealth_mode(self, driver: webdriver.Chrome) -> None:
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )

    def parse(self) -> str:
        self.__set_stealth_opt()
        with self.__chrome(options=self.__chrome_opt) as driver:
            self.__set_stealth_mode(driver)
            driver.get(url=self.__URL)
            self.__handle_page(driver)
        # print(self.__get_str_result())
        # return self.__get_str_result()
        return self.__result

    
    def __format_result(self, prod_list: list[WebElement]) -> None:
        for item in prod_list:
            marker_url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            test_name = item.find_element(By.TAG_NAME, 'h3').text
            if self.__cities.get(self.city) in marker_url.split('/') and self.__name_filter(test_name):
                name = item.find_element(By.TAG_NAME, 'h3').text
                price = item.find_element(By.CSS_SELECTOR, '[itemprop="price"]').get_attribute('content')
                link = self.__shorten_url(item.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                self.__result.append(f'Название: {name}\nЦена: {price}\nСсылка: {link} \n')
    def __handle_page(self, driver: Chrome) -> None: 
        
        search_input: WebElement = driver.find_element(By.CLASS_NAME, 'input-input-Zpzc1')
        search_input.click()
        search_input.send_keys(self.__query)
        search_input.send_keys(Keys.ENTER)
        
        sleep(2)

        driver.find_element(By.XPATH, '//div[@data-marker="search-form/change-location"]').click()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, '//button[@data-marker="popup-location/region/clearButton"]').click()
        city_input: WebElement = driver.find_element(
                    By.XPATH, 
                    '//input[@data-marker="popup-location/region/search-input"]')
        city_input.clear()
        city_input.send_keys(self.__class__.city)
        sleep(2)
        driver.find_element(By.CLASS_NAME, 'suggest-suggest_content-_LYs8').click()
        driver.find_element(By.XPATH, '//button[@data-marker="popup-location/save-button"]').click()
        products: WebElement = driver.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]')
        prod_list: List[WebElement] = products.find_elements(By.XPATH, '//div[@data-marker="item"]')
        self.__format_result(prod_list)

        
        

if __name__ == '__main__':
    p = Parser('amd ryzen 5 3600')
    p.parse()








