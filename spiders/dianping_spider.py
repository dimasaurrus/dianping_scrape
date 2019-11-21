import scrapy
import re
import json
from scrapy.selector import Selector
from googletrans import Translator
# from translate import Translator
# import goslate
from textblob import TextBlob
from selenium import webdriver
from bs4 import BeautifulSoup
import time

translator = Translator()
# translator = Translator(to_lang="en")
# translator = goslate.Goslate()
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"

	# webdrive for selenium
	def __init__(self):
		self.browser = webdriver.PhantomJS()

	# main url dianping
	def start_requests(self):
		yield scrapy.Request(url="http://www.dianping.com", callback=self.get_all_city)

	# get city
	def get_all_city(self, response):
		get_city = response.css("div.clearfix a.city-item::text").extract()

		for loop_city in get_city:
			encode_string = loop_city.encode("utf-8")
			dencode_string = encode_string.decode("utf-8")
			tranlsate_text = translator.translate(dencode_string, dest='en')
			# tranlsate_text = dencode_string.translate(to='en')
			url_by_city = "http://www.dianping.com/"+tranlsate_text.text+"/food"
			yield scrapy.Request(url=url_by_city, callback=self.get_link_restaurant)

	# get link restaurant by city
	def get_link_restaurant(self, response):
		link_list_restaurant = response.css("div.main a.more::attr(href)").extract()[1]
		yield scrapy.Request(url="http://www.dianping.com"+link_list_restaurant, callback=self.get_data_restaurant)

	#get data restaurant
	def get_data_restaurant(self, response):
		vals = list()
		get_city = response.css("div.logo-input div.clearfix a.J-city span::text").extract()
		get_url = response.request.url
		url =  get_url
		self.browser.get(url)
		time.sleep(3) #load page
		html = self.browser.page_source
		soup = BeautifulSoup(html, features='html.parser')
		get_table = soup.find("table")
		for get_link_and_name_restaurant in get_table.select(".J_shopName"):
			tranlsate_text_restaurant = translator.translate(get_link_and_name_restaurant.text, dest="en")
			get_data = {
				"city" : get_city,
				"link_restaunrant" : get_link_and_name_restaurant.get("href"),
				"name_restaurant" : get_link_and_name_restaurant.text
			}
			vals.append(get_data)

		# for get_region_name in get_table.select(".td-mainRegionName"):
		# 	tranlsate_text_region = translator.translate(get_region_name.text, dest="en")
		# 	get_region_data = {
		# 		"link_restaunrant" : tranlsate_text_region.get("href"),
		# 		"name_restaurant" : tranlsate_text_region.text
		# 	}
		# 	vals.append(get_region_data)

		dumps_data = json.dumps(vals, indent=2)
		loads_data = json.loads(dumps_data, encoding='utf-8')
		item_dumps = json.dumps(loads_data, ensure_ascii=False, indent=2)
		print (item_dumps)
		# print (get_table.select(".J_shopName"))
		# print (get_table.select(".td-mainRegionName"))
		# print (get_table.select(".td-refinedScore1"))
		print ("=-=-=-=-=-")
		# stop

		# imgs = soup.findAll('a', attrs={'class': 'J_shopName'})
		# for img in imgs:
		# 	tranlsate_text_restaurant = translator.translate(img.text, dest="en")
		# 	vals = {
		# 		"link_restaunrant" : img.get('href'),
		# 		"name_restaurant" : tranlsate_text_restaurant.text,
		# 	}