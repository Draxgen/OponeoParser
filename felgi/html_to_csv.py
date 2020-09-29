import configparser
import os  # moduł do zarządania systemem
import glob
import re
import shelve
import json
import csv
import time

from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('./felgi/files/selenium_crawler.ini')


def processed(names):
	with shelve.open(config["DEFAULT"]["ProcessedHTMLShelve"]) as items:
		if names in items.keys():
			return True
	return False


def add_processed(names):
	with shelve.open(config["DEFAULT"]["ProcessedHTMLShelve"]) as items:
		items[names] = True


# if __name__ == '__main__':
# 	base_path = config["DEFAULT"]["HTMLFiles"]
# 	files = glob.glob(f'{base_path}*.html')
# 	files.sort(key=os.path.getmtime)

# 	print('start')

# 	for f in files:
# 		print(f)
# 		if processed(f):
# 			print('Skip')
# 			continue
# 		with open(f) as html:
# 			soup = BeautifulSoup(html, "html.parser")
# 			main_objects = soup.select('div.container.item')

# 			#TODO: CENE dobrać

# 			for m in main_objects:
# 				producer = m.select('div.productName > h3 > a > span.producer')[0].get_text()
# 				model = m.select('div.productName > h3 > a > span.model')[0].get_text()
				
# 				diameter = m.select('ul.parameter > li > strong')[0].get_text()
# 				width = m.select('ul.parameter > li > strong')[1].get_text()
# 				central = m.select('ul.parameter > li > strong')[2].get_text()
# 				spacing = m.select('ul.parameter > li > strong')[3].get_text()
# 				et = m.select('ul.parameter > li > strong')[4].get_text()
# 				color = m.select('ul.parameter > li > strong')[5].get_text()
				
# 				# nie w każdym

# 				price = m.select('.price.size-3')
				
# 				if len(price) > 0:
# 					price = price[0].get_text()
# 				else:
# 					price = m.select('.price.size-4')
# 					if len(price) > 0:
# 						price = price[0].get_text()
			

# 				fil = [producer, model, diameter, width, central, spacing, et, color, price]

# 				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
# 					writer = csv.writer(csv_file, delimiter=';')
# 					writer.writerow(fil)
# 		add_processed(f)


def collect_data_f():
	base_path = config["DEFAULT"]["HTMLFiles"]
	files = glob.glob(f'{base_path}*.html')
	files.sort(key=os.path.getmtime)

	print('start')

	for f in files:
		print(f)
		if processed(f):
			print('Skip')
			continue
		with open(f) as html:
			soup = BeautifulSoup(html, "html.parser")
			main_objects = soup.select('div.container.item')

			#TODO: CENE dobrać

			for m in main_objects:
				producer = m.select('div.productName > h3 > a > span.producer')[0].get_text()
				model = m.select('div.productName > h3 > a > span.model')[0].get_text()
				
				diameter = m.select('ul.parameter > li > strong')[0].get_text()
				width = m.select('ul.parameter > li > strong')[1].get_text()
				central = m.select('ul.parameter > li > strong')[2].get_text()
				spacing = m.select('ul.parameter > li > strong')[3].get_text()
				et = m.select('ul.parameter > li > strong')[4].get_text()
				color = m.select('ul.parameter > li > strong')[5].get_text()
				
				# nie w każdym

				price = m.select('.price.size-3')
				
				if len(price) > 0:
					price = price[0].get_text()
				else:
					price = m.select('.price.size-4')
					if len(price) > 0:
						price = price[0].get_text()
			

				fil = [producer, model, diameter, width, central, spacing, et, color, price]

				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
					writer = csv.writer(csv_file, delimiter=';')
					writer.writerow(fil)
		add_processed(f)