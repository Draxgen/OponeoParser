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
config.read('./motocykle/files/selenium_crawler.ini')


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
				
# 				axis = m.find('span', {'class': 'axle'})
# 				if axis:
# 					axis = axis.get_text().strip()
				
# 				parameters = m.select('ul.parameter > li > strong')	
				
# 				if len(parameters) > 3:
# 					type_tire = parameters[1].get_text().strip()
# 					type_base = parameters[2].get_text().strip()
				
# 				last_type = ''
# 				if len(parameters) == 4:
# 					last_type = parameters[3].get_text().strip()
				
# 				# nie w każdym

# 				price = m.select('.price.size-3')
				
# 				if len(price) > 0:
# 					price = price[0].get_text()
# 				else:
# 					price = m.select('.price.size-4')
# 					if len(price) > 0:
# 						price = price[0].get_text()
			
# 				matchSzie = re.match(r'^\d+/\d+\w+ \w+\d+', size)
# 				if matchSzie:
# 					diameter = re.findall(r'\s\w+\d+', size)[0].strip()
# 					width = re.findall(r'^\d+/', size)[0][0:-1].strip()
# 					profile = re.findall(r'/\d+\w+\s', size)[0][1: -1]
# 				else:
# 					matchSzie = re.match(r'^\d+/\d+-\d+', size)
# 					if matchSzie:
# 						diameter = re.findall(r'-\d+', size)[0].strip()
# 						width = re.findall(r'^\d+/', size)[0][0:-1].strip()
# 						profile = re.findall(r'/\d+-', size)[0][1: -1]

# 				try:
# 					year = m.select('div.buy > div.dot')[0].get_text().strip()
# 					# print('rok',year.splitlines())
# 					year_re = re.findall(r'\d+', year)[0].strip()
# 					year = year_re
# 					try:
					
# 						country = m.select('div.buy > div.dot > span.country')[0].get_text().strip()
# 						year = f'{year} - {country}'
# 					except IndexError:
# 						pass

# 				except IndexError:
# 					year = ''

				

# 				if season == 'SeasonAllSeason':
# 					season = 'całoroczne'
# 				elif season == 'SeasonWinter':
# 					season = 'zimowe'
# 				elif season == 'SeasonSummer':
# 					season = 'letnie'
# 				else:
# 					season = ''
# 				print(producer, model, size)

# 				fil = [producer, model, width, profile, diameter, load_index, speed_index, axis, type_tire, type_base,
# 				       last_type, year, season, price]

# 				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
# 					writer = csv.writer(csv_file, delimiter=';')
# 					writer.writerow(fil)
# 		add_processed(f)


def collect_data_m():
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
				size = m.select('div.productName > h3 > a > span.size')[0].get_text()
				load_index = m.find('span', {'data-tp': 'TireLoadIndex'})
				speed_index = m.find('span', {'data-tp': 'TireSpeedIndex'})
				if speed_index:
					speed_index = speed_index.get_text().strip()
				if load_index:
					load_index = load_index.get_text().strip()
				season = m.select('div.column > div.icon.season')[0]['data-tp']
				
				axis = m.find('span', {'class': 'axle'})
				if axis:
					axis = axis.get_text().strip()
				
				parameters = m.select('ul.parameter > li > strong')	
				
				type_tire = ''
				type_base = ''
				if len(parameters) > 3:
					type_tire = parameters[1].get_text().strip()
					type_base = parameters[2].get_text().strip()
				
				last_type = ''
				if len(parameters) == 4:
					last_type = parameters[3].get_text().strip()
				
				# nie w każdym

				price = m.select('.price.size-3')
				
				if len(price) > 0:
					price = price[0].get_text()
				else:
					price = m.select('.price.size-4')
					if len(price) > 0:
						price = price[0].get_text()
			
				matchSzie = re.match(r'^\d+/\d+\w+ \w+\d+', size)

				diameter = ''
				width = ''
				profile = ''

				if matchSzie:
					diameter = re.findall(r'\s\w+\d+', size)[0].strip()
					width = re.findall(r'^\d+/', size)[0][0:-1].strip()
					profile = re.findall(r'/\d+\w+\s', size)[0][1: -1]
				else:
					matchSzie = re.match(r'^\d+/\d+-\d+', size)
					if matchSzie:
						diameter = re.findall(r'-\d+', size)[0].strip()
						width = re.findall(r'^\d+/', size)[0][0:-1].strip()
						profile = re.findall(r'/\d+-', size)[0][1: -1]

				try:
					year = m.select('div.buy > div.dot')[0].get_text().strip()
					# print('rok',year.splitlines())
					year_re = re.findall(r'\d+', year)[0].strip()
					year = year_re
					try:
					
						country = m.select('div.buy > div.dot > span.country')[0].get_text().strip()
						year = f'{year} - {country}'
					except IndexError:
						pass

				except IndexError:
					year = ''

				

				if season == 'SeasonAllSeason':
					season = 'całoroczne'
				elif season == 'SeasonWinter':
					season = 'zimowe'
				elif season == 'SeasonSummer':
					season = 'letnie'
				else:
					season = ''
				print(producer, model, size)

				fil = [producer, model, width, profile, diameter, load_index, speed_index, axis, type_tire, type_base,
				       last_type, year, season, price]

				with open(config["DEFAULT"]["CSVFile"], 'a+') as csv_file:
					writer = csv.writer(csv_file, delimiter=';')
					writer.writerow(fil)
		add_processed(f)