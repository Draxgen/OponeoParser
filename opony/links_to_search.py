import configparser
import re

config = configparser.ConfigParser()
config.read('files/selenium_crawler.ini')



with open(config["DEFAULT"]["LinksPath"], 'r') as fp:
    print(fp)

    line = fp.readlines()
    line_position = 1  
    
    for l in line:
        base_link = 'https://www.oponeo.pl/wybierz-opony/r=1/'

        check_c = re.search(r'/ciezarowe/', l)

        if not check_c:
            find_base = re.search(r'\d+/\d+/r\d+', l)

            if find_base:
                one = re.search(r'^\d+/', find_base[0])
                two = re.search(r'/\d+/', find_base[0])
                r = re.search(r'/r\d+', find_base[0])
                print(one[0][0:-1])
                print(two[0][1:-1])
                print(r[0][1:])

                output_link = f'{base_link}{one[0][0:-1]}-{two[0][1:-1]}-{r[0][1:]}'
                print(output_link)
                with open('./files/test.txt', 'a') as new_file:
                    output_link = output_link + '\n'
                    new_file.write(output_link)