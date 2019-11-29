import scrapy
import re
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from collections import defaultdict
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http.cookies import CookieJar
from dianping_scrape.items import RestaurantItem
from scrapy.selector import Selector

list_restaurant_by_city = {}
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"
	handle_httpstatus_all = [302]

	# --- webdrive for selenium ---
	def __init__(self):
		self.browser = webdriver.PhantomJS()

	# --- main url dianping ---
	def start_requests(self):
		yield scrapy.Request(url="http://www.dianping.com", callback=self.get_all_city)

	# -- check cookies --
	def _method_check_coockies(self, val_cookies):
		split_str_cookie = dict(item.split("=") for item in val_cookies.split(";"))
		return split_str_cookie

	# --- get city ---
	def get_all_city(self, response):
		# get_city = response.css("div.clearfix a.city-item::text").extract()
		get_city = response.css("div.clearfix a.city-item::attr(href)").extract()

		for loop_city in get_city:
			url_by_city = loop_city.replace("//", "http://")
			yield scrapy.Request(url=url_by_city+"/food", callback=self.get_link_restaurant)

	# --- get link restaurant by city ---
	def get_link_restaurant(self, response):
		try:
			link_list_restaurant = response.css("div.main a.more::attr(href)").extract()[1]
			yield scrapy.Request(url="http://www.dianping.com"+link_list_restaurant, callback=self.get_data_restaurant)
		except IndexError:
			pass

	# --- get data restaurant ---
	def get_data_restaurant(self, response):
		get_city = response.css("div.logo-input div.clearfix a.J-city span::text").extract()
		get_tag_div = response.css("div.tit")
		for get_type_link in get_tag_div:
			for get_link_restaurant in get_type_link.css("a::attr(href)").extract():
				yield scrapy.Request(url=get_link_restaurant+"/dishlist", callback=self.get_menu_data)
		# restaurant_item = RestaurantItem()

		# url =  get_url
		# self.browser.get(url)
		# html = self.browser.page_source
		# soup = BeautifulSoup(html, features='html.parser')

		# -- tested --
		# get_table = soup.find("table")
		# get_menus= soup.find_all("div", {"class": "tit"})
		# print (get_menus)
		# print (get_menu_url)
		# print (get_data)

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
	def get_menu_data(self, response):
		print ("MASUK")
		get_menu_url = response.request.url
		name_restaurant = response.css("div.list-desc div.list-desc")
		for get_data in name_restaurant.extract():
			print (get_data.css("a::attr(href)").extract())
			print (get_data.css("div.shop-food-img::text").extract())
			print (get_data.css("div.shop-food-img img::attr(src)").extract())
			print (get_data.css("svgmtsi.dishName::text").extract())
			print ("TTTTTTTTTTTTTTT")


if __name__ == "__main__":
	process = CrawlerProcess(get_project_settings())
	process.crawl('dianping_spider')
	process.start()		