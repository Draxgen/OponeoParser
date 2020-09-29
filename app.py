import os
import time
import datetime
import shutil
from subprocess import check_output, call
from opony.selenium_crawler import opony_app
from opony.html_to_csv import collect_data

from motocykle.selenium_crawler import motocykle_app
from motocykle.html_to_csv import collect_data_m

from felgi.selenium_crawler import felgi_app
from felgi.html_to_csv import collect_data_f

from alufelgi.selenium_crawler import alufelgi_app
from alufelgi.html_to_csv import collect_data_a

from webdrivermanager import ChromeDriverManager
import pyderman as dr

if __name__ == '__main__':

    print('\n1. Aktualizacja drivera. \n\n2. Parser opon. \n21. Opony do csv. '+
    '\n\n3. Parser motocykle. \n31. Motocykle do csv. \n\n4. Parser felg. \n41. Felgi do csv'+
    ' \n\n5. Parser alufelgi \n51 Alufelgi do csv')
    
    number = input('Wybierz numer: ')

    if number == '1':
        print('Aktualizacja drivera')
        # chd = ChromeDriverManager()
        # chd.download_and_install()
        # path = os.path.join(os.getcwd(), 'driver')
        # call(['webdrivermanager', 'chrome', f'-d {str(path)}'])
        # print(s)
        path = dr.install(browser=dr.chrome, file_directory=os.getcwd(), overwrite=True, filename='chromedriver')
        print(f'Zainstalowano : ${path}')
        print('Kopiowanie do C:\Windows')
        shutil.copy2(path, 'C:\Windows')
        
    elif number == '2':
        print('\n PARSER OPON \n')
        start_time = time.time()
        print(f'Czas rozpoczęcia: {start_time}')
        path = os.path.join(os.getcwd(), 'opony')
        os.chdir(path)
        opony_app()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')
    elif number == '21':
        print('\n OBRÓBKA OPON DO CSV \n')
        start_time = time.time()
        path = os.path.join(os.getcwd(), 'opony')
        os.chdir(path)
        collect_data()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')

    elif number == '3':
        print('\n PARSER MOTOCYKLE \n')
        start_time = time.time()
        print(f'Czas rozpoczęcia: {start_time}')
        path = os.path.join(os.getcwd(), 'motocykle')
        os.chdir(path)
        motocykle_app()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')
    elif number == '31':
        print('\n OBRÓBKA MOTOCYKLI DO CSV \n')
        path = os.path.join(os.getcwd(), 'motocykle')
        os.chdir(path)
        collect_data_m()

    elif number == '4':
        print('\n PARSER FELG \n')
        start_time = time.time()
        print(f'Czas rozpoczęcia: {start_time}')
        path = os.path.join(os.getcwd(), 'felgi')
        os.chdir(path)
        felgi_app()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')
    elif number == '41':
        print('\n OBRÓBKA FELG DO CSV \n')
        start_time = time.time()
        path = os.path.join(os.getcwd(), 'felgi')
        os.chdir(path)
        collect_data_f()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')

    elif number == '5':
        print('\n PARSER ALUFELG \n')
        start_time = time.time()
        print(f'Czas rozpoczęcia: {start_time}')
        path = os.path.join(os.getcwd(), 'alufelgi')
        os.chdir(path)
        alufelgi_app()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')
    elif number == '51':
        print('\n OBRÓBKA FELG DO CSV \n')
        start_time = time.time()
        path = os.path.join(os.getcwd(), 'alufelgi')
        os.chdir(path)
        collect_data_a()
        end_time = time.time() - start_time
        print(f'Trwało: {datetime.timedelta(seconds=end_time)}')    
        
    else:
        pass