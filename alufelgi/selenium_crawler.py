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
from random import randint  # moduł losujący randomową liczbę w przedziale

config = configparser.ConfigParser()
config.read('./alufelgi/files/selenium_crawler.ini')


def prepare_driver():
    """
    Funkcja odpowiedzialna za skonfigurowanie proxy
    oraz otworzenie przeglądarki
    :return: webdriver
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(
        chrome_options=chrome_options
    )


def go_to_page(driver, page):
    """
    Funkcja dzięki której nasz webdriver
    przechodzi na podaną podstronę.
    :param driver: nasz driver
    :param page: strona na którą ma przejść
    :return:
    """

    driver.get(page)
    time.sleep(randint(1, 3))  # program usypia na losową ilość sekund w przedziale 1, 4


def processed(names):
    """
    Funkcja sprawdza czy w shelve jest dany link
    jesli jest to zwraca True i przez to
    crawler pomija ten link i sprawdza nastepny
    :param names: nasz link
    """
    with shelve.open(config["DEFAULT"]["ProcessedShelve"]) as items:
        if names in items.keys():
            return True
    return False


def add_processed(names):
    """
   Funkcja dodaje link do naszego shelve
   :param names: nasz link
   """
    with shelve.open(config["DEFAULT"]["ProcessedShelve"]) as items:
        items[names] = True


def check_scroll(browser):
    """
    Funkcja sprawdza czy jest przycisk
    który rozwija liste opon dopóki ten
    przycisk się pojawia funkcja będzię
    się wykonywać.
    """

    while True:
        print('Check Scroll')
        try:
            element = browser.find_element_by_xpath('//div[@class="container loadMore"]/a')
            actions = ActionChains(browser)  # https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html
            actions.move_to_element(element).perform()  # scrollowanie do przycisku
            element.click()  # kliknięcie przycisku
            time.sleep(2)
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            break  # https://www.programiz.com/python-programming/break-continue


def prepare_path():
    """
    Funkcja która przygotowuje nam
    siceżkę do pliku w którym zapiszemy html
    """
    base_path = config["DEFAULT"]["HTMLFiles"]
    files = glob.glob(f'{base_path}*.html')  # https://docs.python.org/3/library/glob.html
    files.sort(key=os.path.getmtime)  # posortowanie plików po datcie
    return_file = files[-1]  # wybranie najnowszego pliku
    size_of_file = os.path.getsize(return_file)  # sprawdzanie wielkosci pliku

    if size_of_file >= 2000000:  # jesli plik jest wiekszy od 2mb to tworzy nowy
        file_name = os.path.basename(return_file)
        file_number = os.path.splitext(file_name)[0]
        new_filename = int(file_number) + 1
        return_file = f'{base_path}{new_filename}.html'

    return return_file


def write_result(result, file):
    """
    Funkcja która zapisuje html
    do pliku
    """
    if not result.endswith('\n'):
        result = result + '\n'
    with open(file, 'a+', encoding='utf-8') as f:
        if result:
            f.write(result)


def prepare_html(browser):
    """
     Funkcja która przygotowuje html
     do zapisania
     """
    html_obj = browser.find_elements_by_xpath('//div[@id="productList"]')  # znalezienie listy opon
    if len(html_obj) == 0:
        return False
    h_path = prepare_path()
    for html in html_obj:
        write_result(html.get_attribute('innerHTML'), h_path)


def is_next_page(driver):
    try:
        element = driver.find_element_by_xpath('//a[contains(@title, "Strona")]')
        return element
    except NoSuchElementException:
        return False

def paginate(driver, page):
    element = driver.find_elements_by_xpath('//a[contains(@title, "Strona")]')
    actions = ActionChains(driver) 
    if page == 1:
        actions.move_to_element(element[0]).perform()
        try:  
            element[0].click()
        except ElementClickInterceptedException:
            pass
    else:
        if len(element) > 1:
            try: 
                try:
                    actions.move_to_element(element[1]).perform()  
                    element[1].click()
                except ElementClickInterceptedException:
                    pass
            except StaleElementReferenceException:
                pass
        else:
            try: 
                actions.move_to_element(element[0]).perform()  
                element[0].click()
            except StaleElementReferenceException:
                pass


    time.sleep(randint(1, 3))

def is_last_page(driver):
    print('Check last page')
    try:
        element = driver.find_element_by_xpath('//a[contains(@title, "Ostatnia strona")]')
        return True
    except NoSuchElementException:
        return False


# if __name__ == '__main__':  
#     driver = prepare_driver()  
#     with open(config["DEFAULT"]["LinksPath"], 'r') as fp:  
#         line = fp.readlines()  
#         line_position = 1  
#         for l in line:  
#             if processed(l):
#                 line_position += 1
#                 continue

#             print(f'{line_position} of {len(line)} : {l}')  
#             go_to_page(driver, l)
#             check_scroll(driver)
#             prepare_html(driver)

#             add_processed(l)
#             line_position += 1  
#             time.sleep(1)

#     driver.close()

def alufelgi_app():
    driver = prepare_driver()  
    with open(config["DEFAULT"]["LinksPath"], 'r') as fp:  
        line = fp.readlines()  
        line_position = 1  
        for l in line:  
            if processed(l):
                line_position += 1
                continue

            print(f'{line_position} of {len(line)} : {l}')  
            go_to_page(driver, l)
            check_scroll(driver)
            prepare_html(driver)

            add_processed(l)
            line_position += 1  
            time.sleep(1)

    driver.close()
