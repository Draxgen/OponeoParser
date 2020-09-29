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
config.read('./opony/files/selenium_crawler.ini')


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
# 				size = m.select('div.productName > h3 > a > span.size')[0].get_text()
# 				load_index = m.find('span', {'data-tp': 'TireLoadIndex'})
# 				speed_index = m.find('span', {'data-tp': 'TireSpeedIndex'})
# 				if speed_index:
# 					speed_index = speed_index.get_text().strip()
# 				if load_index:
# 					load_index = load_index.get_text().strip()
# 				season = m.select('div.column > div.icon.season')[0]['data-tp']
# 				sticker = m.find('div', {'data-tp': 'TooltipUe'})
# 				sticker = m.find('div', {'data-tp': 'TooltipUe'})
# 				print(f'{producer} - {sticker}')
# 				# nie w każdym
# 				run_flat = m.find('span', {'data-tp': 'TireROF'})
# 				c = m.find('span', {'data-tp': 'TireCargo'})
# 				xl = m.find('span', {'data-tp': 'TireEXtraLoad'})

# 				price = m.select('.price.size-3')
				
# 				if len(price) > 0:
# 					price = price[0].get_text()
# 				else:
# 					price = m.select('.price.size-4')
# 					if len(price) > 0:
# 						price = price[0].get_text()
			
# 				matchSzie = re.match(r'^\d+/\d+ R\d+', size)
# 				if matchSzie:
# 					diameter = re.findall(r'\sR\d+', size)[0].strip()
# 					width = re.findall(r'^\d+/', size)[0][0:-1].strip()
# 					profile = re.findall(r'/\d+\s', size)[0][1: -1]

# 				try:
# 					year = m.select('div.productName > h3 > span.dot')[0].get_text().strip()
# 					year_re = re.findall(r'\d+', year)[0].strip()
# 					year = year_re
# 				except IndexError:
# 					year = ''

# 				if sticker:
# 					sticker_json = json.loads(sticker['data-tpd'].replace("'", '"'))
# 					fuel = sticker_json[0]['@MSG1']
# 					rain = sticker_json[0]['@MSG2']
# 					noise = sticker_json[0]['@MSG3']
# 				else:
# 					fuel = ''
# 					rain = ''
# 					noise = ''

# 				if c:
# 					c = 'Tak'
# 				else:
# 					c = ''
# 				if xl:
# 					xl = 'Tak'
# 				else:
# 					xl = ''
# 				if run_flat:
# 					run_flat = 'Tak'
# 				else:
# 					run_flat = ''

# 				if season == 'SeasonAllSeason':
# 					season = 'całoroczne'
# 				elif season == 'SeasonWinter':
# 					season = 'zimowe'
# 				elif season == 'SeasonSummer':
# 					season = 'letnie'
# 				else:
# 					season = ''

# 				fil = [producer, model, width, profile, diameter, load_index, speed_index, c, fuel, rain, noise,
# 				       year, season, run_flat, xl, price]

# 				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
# 					writer = csv.writer(csv_file, delimiter=';')
# 					writer.writerow(fil)
# 		add_processed(f)


def collect_data():
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

				if 'bica' in producer:
					print('name')
					producer = 'Dębica'
				model = m.select('div.productName > h3 > a > span.model')[0].get_text()
				size = m.select('div.productName > h3 > a > span.size')[0].get_text()
				load_index = m.find('span', {'data-tp': 'TireLoadIndex'})
				speed_index = m.find('span', {'data-tp': 'TireSpeedIndex'})
				if speed_index:
					speed_index = speed_index.get_text().strip()
				if load_index:
					load_index = load_index.get_text().strip()
				season = m.select('div.column > div.icon.season')[0]['data-tp']
				sticker = m.find('div', {'data-tp': 'TooltipUe'})
				sticker = m.find('div', {'data-tp': 'TooltipUe'})
				print(f'{producer} - {sticker}')

				homologation = m.find('span', {'class': 'homologation'})
				if homologation:
					homologation = homologation.get_text().strip()

				run_flat = m.find('span', {'data-tp': 'TireROF'})
				c = m.find('span', {'data-tp': 'TireCargo'})
				xl = m.find('span', {'data-tp': 'TireEXtraLoad'})
				rf = m.find('span', {'data-tp': 'TireRainforced'})

				price = m.select('.price.size-3')
				
				if len(price) > 0:
					price = price[0].get_text()
				else:
					price = m.select('.price.size-4')
					if len(price) > 0:
						price = price[0].get_text()
			
				matchSzie = re.match(r'^\d+/\d+ R\d+', size)
				if matchSzie:
					diameter = re.findall(r'\sR\d+', size)[0].strip()
					width = re.findall(r'^\d+/', size)[0][0:-1].strip()
					profile = re.findall(r'/\d+\s', size)[0][1: -1]

				try:
					year = m.select('div.productName > h3 > span.dot')[0].get_text().strip()
					year_re = re.findall(r'\d+', year)[0].strip()
					year = year_re
				except IndexError:
					year = ''

				if sticker:
					sticker_json = json.loads(sticker['data-tpd'].replace("'", '"'))
					fuel = sticker_json[0]['@MSG1']
					rain = sticker_json[0]['@MSG2']
					noise = sticker_json[0]['@MSG3']
				else:
					fuel = ''
					rain = ''
					noise = ''

				if c:
					c = 'C'
				else:
					c = ''
				if xl:
					xl = 'XL'
				else:
					xl = ''
				if run_flat:
					run_flat = 'Tak'
				else:
					run_flat = ''
				if rf:
					xl = 'RF'

				if season == 'SeasonAllSeason':
					season = 'całoroczna'
				elif season == 'SeasonWinter':
					season = 'zima'
				elif season == 'SeasonSummer':
					season = 'lato'
				else:
					season = ''

				fil = [producer, model, width, profile, diameter, load_index, speed_index, c, fuel, rain, noise,
				       year, season, run_flat, xl, homologation, price]

				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
					writer = csv.writer(csv_file, delimiter=';')
					writer.writerow(fil)
		add_processed(f)