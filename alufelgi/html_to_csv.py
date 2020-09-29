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
config.read('./alufelgi/files/selenium_crawler.ini')


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
# 		with open(f, 'rb') as html:
# 			soup = BeautifulSoup(html, "html.parser")
# 			main_objects = soup.select('div.item')

			
# 			for m in main_objects:
# 				print('ok')
# 				producer = m.select('div.productName > h3 > a > span.producer')[0].get_text()
# 				model = m.select('div.productName > h3 > a > span.model')[0].get_text()

# 				base_text = m.select('div.productName > h3 > a ')[0]['title']

# 				print(base_text)
			
				
# 				diameter = re.findall(r'\d+x\d+\s', base_text)[0].strip()
# 				diameter = re.findall(r'\d+', diameter)[1]
# 				print(diameter)

# 				width = re.findall(r'\d+,\d+x\d+\s', base_text)[0].strip()
# 				width = re.findall(r'\d+,\d+', width)[0]
# 				print(width)

# 				spacing = ''
# 				try:
# 					spacing = re.findall(r'\d+x\d+,\d+', base_text)[0].strip()
# 				except IndexError:
# 					try:
# 						spacing = re.findall(r'\d+x\d+.\d+', base_text)[0].strip()
# 					except IndexError:
# 						pass
# 				print(spacing)

# 				et = ''
# 				try:
# 					et = re.findall(r'ET\d+,\d+', base_text)[0].strip()
# 					et = re.findall(r'\d+,\d+', et)[0].strip()
# 				except IndexError:
# 					pass
# 				print(et)

# 				color = m.select('ul.parameter > li > strong')[0].get_text()
				

# 				price = m.select('.price.size-3')
				
# 				if len(price) > 0:
# 					price = price[0].get_text()
# 				else:
# 					price = m.select('.price.size-4')
# 					if len(price) > 0:
# 						price = price[0].get_text()
			

# 				fil = [producer, model, diameter, width, spacing, et, color, price]

# 				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
# 					writer = csv.writer(csv_file, delimiter=';')
# 					writer.writerow(fil)
# 		add_processed(f)


def collect_data_a():
	base_path = config["DEFAULT"]["HTMLFiles"]
	files = glob.glob(f'{base_path}*.html')
	files.sort(key=os.path.getmtime)

	print('start')

	for f in files:
		print(f)
		if processed(f):
			print('Skip')
			continue
		with open(f, 'rb') as html:
			soup = BeautifulSoup(html, "html.parser")
			main_objects = soup.select('div.item')

			
			for m in main_objects:
				print('ok')
				producer = m.select('div.productName > h3 > a > span.producer')[0].get_text()
				model = m.select('div.productName > h3 > a > span.model')[0].get_text()

				base_text = m.select('div.productName > h3 > a ')[0]['title']

				print(base_text)
			
				
				diameter = re.findall(r'\d+x\d+\s', base_text)[0].strip()
				diameter = re.findall(r'\d+', diameter)[1]
				print(diameter)

				width = re.findall(r'\d+,\d+x\d+\s', base_text)[0].strip()
				width = re.findall(r'\d+,\d+', width)[0]
				print(width)

				spacing = ''
				try:
					spacing = re.findall(r'\d+x\d+,\d+', base_text)[0].strip()
				except IndexError:
					try:
						spacing = re.findall(r'\d+x\d+.\d+', base_text)[0].strip()
					except IndexError:
						pass
				print(spacing)

				et = ''
				try:
					et = re.findall(r'ET\d+,\d+', base_text)[0].strip()
					et = re.findall(r'\d+,\d+', et)[0].strip()
				except IndexError:
					pass
				print(et)

				color = m.select('ul.parameter > li > strong')[0].get_text()
				

				price = m.select('.price.size-3')
				
				if len(price) > 0:
					price = price[0].get_text()
				else:
					price = m.select('.price.size-4')
					if len(price) > 0:
						price = price[0].get_text()
			

				fil = [producer, model, diameter, width, spacing, et, color, price]

				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
					writer = csv.writer(csv_file, delimiter=';')
					writer.writerow(fil)
		add_processed(f)