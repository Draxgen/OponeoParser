import time  # moduł odpowiedizalny za czas
import os  # moduł do zarządania systemem
import glob
import shelve  # https://docs.python.org/3/library/shelve.html
import configparser  # importowanie modułu który pozwala odczytwyać pliki .ini odpowiedzialny za ustawienia [https://docs.python.org/3/library/configparser.html]

from selenium import webdriver  # importowanie webdrivera selenium [https://selenium-python.readthedocs.io/getting-started.html]
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from random import randint  # moduł losujący randomową liczbę w przedziale

config = configparser.ConfigParser()
config.read('files/selenium_crawler.ini')


def prepare_driver():
    """
    Funkcja odpowiedzialna za skonfigurowanie proxy
    oraz otworzenie przeglądarki
    :return: webdriver
    """
    headless_proxy = "127.0.0.1:3128"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': headless_proxy,
        'ftpProxy': headless_proxy,
        'sslProxy': headless_proxy,
        'noProxy': ''
    })

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    capabilities = dict(DesiredCapabilities.CHROME)

    # capabilities["marionette"] = False
    proxy.add_to_capabilities(capabilities)

    print(capabilities)

    # słowo return zwracam nam wartość danej funkcji w tym przypadku zwraca nam webdriver chroma czyli otwiera przeglądarke
    return webdriver.Chrome(
        './drivers/chromedriver_linux/chromedriver',
    )




if __name__ == '__main__':  # https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    driver = prepare_driver()  # przypisanie wyniku z funkcji prepare_driver do zmiennej driver
    driver.get('https://www.oponeo.pl/wybierz-opony-motocyklowe')
    
    width = Select(driver.find_element_by_xpath('//select[@id="_ctTS_ddlDimWidth"]'))
    print(width)

    driver.close()

