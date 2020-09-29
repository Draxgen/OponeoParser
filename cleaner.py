import os
import shutil

def remove_all(section):
    print('Usuwanie shelve:')
    try:
        os.remove(f'./{section}/files/processed.db')
    except OSError:
        pass   
    try:
        os.remove(f'./{section}/files/processed_html.db')
    except OSError:
        pass

    print('Usuwani html_files')
    try:
        shutil.rmtree(f'./{section}/html_files')
    except FileNotFoundError:
        pass

    os.mkdir(f'./{section}/html_files')
    open(f'./{section}/html_files/1.html', 'x')

    print('Usuwanie csv')
    try:
        os.remove(f'./{section}/html_output/data.csv')
    except OSError:
        pass

    shutil.copy2(f'./{section}/html_output/layout.csv', f'./{section}/html_output/data.csv')

if __name__ == '__main__':
    print('Rozpoczynam czyszczenie')
    
    print('Opony')
    remove_all('opony')

    print('Motocykle')
    remove_all('motocykle')

    print('Felgi')
    remove_all('felgi')
    
    print('Alufelgi')
    remove_all('alufelgi')
    


   