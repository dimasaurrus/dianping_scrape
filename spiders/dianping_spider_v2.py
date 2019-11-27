import scrapy
import re
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dianping_scrape.items import RestaurantItem


list_restaurant_by_city = {}
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"

	# --- webdrive for selenium ---
	def __init__(self):
		self.browser = webdriver.PhantomJS()

	# --- main url dianping ---
	def start_requests(self):
		yield scrapy.Request(url="http://www.dianping.com", callback=self.get_all_city)

	# --- get city ---
	def get_all_city(self, response):
		# get_city = response.css("div.clearfix a.city-item::text").extract()
		get_city = response.css("div.clearfix a.city-item::attr(href)").extract()

		for loop_city in get_city:
			url_by_city = loop_city.replace("//", "http://")
			yield scrapy.Request(url=url_by_city+"/food", callback=self.get_link_restaurant)

	# --- get link restaurant by city ---
	def get_link_restaurant(self, response):
		link_list_restaurant = response.css("div.main a.more::attr(href)").extract()[1]
		yield scrapy.Request(url="http://www.dianping.com"+link_list_restaurant, callback=self.get_data_restaurant)

	# --- get data restaurant ---
	def get_data_restaurant(self, response):
		# print ("PASS")
		time.sleep(240) #load page
		global list_restaurant_by_city
		get_city = response.css("div.logo-input div.clearfix a.J-city span::text").extract()
		get_url = response.request.url
		url =  get_url
		self.browser.get(url)
		html = self.browser.page_source
		soup = BeautifulSoup(html, features='html.parser')
		
		# -- tested --
		# get_table = soup.find("table")
		get_menus= soup.find_all("div", {"class": "tit"})
		get_data = get_menus.select(".tit")

		# restaurant_item = RestaurantItem()
		# for get_link_and_name_restaurant in get_table.select(".J_shopName"):
		# 	restaurant_item["city"] = get_city[0]
		# 	restaurant_item["restaurant_url"] = get_link_and_name_restaurant.get("href")
		# 	restaurant_item["link_menus"] = get_link_and_name_restaurant.get("href") + "/dishlist"
		# 	restaurant_item["name_restaurant"] = get_link_and_name_restaurant.text
		# 	yield scrapy.Request(url=get_link_and_name_restaurant.get("href") + "/dishlist", callback=self.get_menu_data)

			# vals = {
			# 	"city" : get_city[0],
			# 	"restaurant_url" : get_link_and_name_restaurant.get("href"),
			# 	"link_list_menus" : get_link_and_name_restaurant.get("href") + "/dishlist",
			# 	"name_restaurant" : get_link_and_name_restaurant.text
			# }

			# if vals["city"] in list_restaurant_by_city:
			# 	list_restaurant_by_city[ vals["city"] ].append(vals)
			# else:				
			# 	list_restaurant_by_city[ vals["city"] ] = []
			# 	list_restaurant_by_city[ vals["city"] ].append(vals)

		# for get_region_restaurant in get_table.select(".td-mainRegionName"):
		# 	regions = get_region_restaurant.text
		# 	if get_city[0] in list_restaurant_by_city:
		# 		for key in list_restaurant_by_city:
		# 			for value_dict in list_restaurant_by_city[key]:
						# restaurant_item["region"] = get_link_and_name_restaurant.text
						# value_dict.update({"region" : regions})

		# for get_value_taste_restaurant in get_table.select(".td-refinedScore1"):
		# 	value_taste = get_value_taste_restaurant.text
		# 	if get_city[0] in list_restaurant_by_city:
		# 		for key in list_restaurant_by_city:
		# 			for value_dict in list_restaurant_by_city[key]:
		# 				restaurant_item["taste"] = get_link_and_name_restaurant.text
						# value_dict.update({"taste" : value_taste})

		# yield restaurant_item

		# dumps_data = json.dumps(list_restaurant_by_city, indent=2)
		# loads_data = json.loads(dumps_data, encoding='utf-8')
		# item_dumps = json.dumps(loads_data, ensure_ascii=False, indent=2)


	# --- get data menu by link ---
	# def get_menu_data(self, response):
	# 	get_menu_url = response.request.url
	# 	self.browser.get(get_menu_url)
	# 	time.sleep(3) #load page
	# 	html = self.browser.page_source
	# 	soup = BeautifulSoup(html, features='html.parser')
	# 	get_menus= soup.findAll("div", {"class": "shop-food-main"})

if __name__ == "__main__":
	process = CrawlerProcess(get_project_settings())
	process.crawl('dianping_spider')
	process.start()		