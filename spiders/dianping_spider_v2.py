import scrapy
import re
import json
import nltk
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from lxml.html import fromstring
from collections import defaultdict
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http.cookies import CookieJar
from dianping_scrape.items import RestaurantItem
from scrapy.selector import Selector

headerInfo = {'content-type': 'application/json' }

list_restaurant_by_city = {}
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"
	handle_httpstatus_list = [301, 302]

	# --- webdrive for selenium ---
	def __init__(self):
		self.browser = webdriver.PhantomJS()

	def _get_ip_proxy(self):
		url = 'https://free-proxy-list.net/'
		response = requests.get(url)
		parser = fromstring(response.text)
		list_ip = []
		for i in parser.xpath('//tbody/tr')[:20]:
			get_ip = i.xpath('.//td[1]/text()')[0]
			get_port = i.xpath('.//td[2]/text()')[0]
			ip_n_port = str(get_ip)+":"+str(get_port)
			list_ip.append(ip_n_port)
		return list_ip


	# --- url list of city ---
	def start_requests(self):
		# get_list_ip = self._get_ip_proxy()
		# yield scrapy.Request(url="http://www.dianping.com", callback=self.get_all_city)
		start_urls = [
			"http://www.dianping.com/citylist"
		]

		# for loop_ip in get_list_ip:
		req= scrapy.Request(
			url=start_urls[0], 
			callback=self.get_all_city,
			# meta={"proxy": "http://"+loop_ip}
		)
		# req.headers['Cookie'] = 'js_enabled=true; is_cookie_active=true;'
		yield req

	# --- get link food by city ---
	def get_all_city(self, response):
		# === First Version ==
		# get_city = response.css("div.clearfix a.city-item::attr(href)").extract()

		# === second version ==
		get_city = response.css("div.findHeight a.onecity::attr(href)").extract()

		for loop_city in get_city:
			url_by_city = loop_city.replace("//", "http://")
			yield scrapy.Request(url=url_by_city+"/food", callback=self.get_link_restaurant)

	# --- get list restaurant by city ---
	def get_link_restaurant(self, response):
		# for get_review_restaurant in response.css("div.popular-nav ul.Fix a::attr(title)").extract():
		if response.css("div.popular-nav ul.Fix"):
			for loop_restaurant in response.css("div.popular-nav ul.Fix"):
				for get_review_restaurant in loop_restaurant.css("a").extract():
					soup = BeautifulSoup(get_review_restaurant, features='html.parser')
					for a in soup.find_all('a'):
						try:
							if a['title'] == "评价餐厅":
								yield scrapy.Request(url="http://www.dianping.com"+a['href'] ,callback=self.get_data_restaurant)
						except:
							pass
		else:
			pass

	# --- get link restaurant ---
	def get_data_restaurant(self, response):
		get_url = response.request.url
		self.browser.get(get_url)
		html = self.browser.page_source
		soup = BeautifulSoup(html, features='html.parser')
		get_table = soup.find("table")
		try:
			for get_link_and_name_restaurant in get_table.select(".J_shopName"):
				get_link = get_link_and_name_restaurant.get("href")
				yield scrapy.Request(url=get_link+"/dishlist", callback=self.get_list_menu_restaurant)
		except AttributeError:
			pass

		# get_tag_div = response.css("div.tit")
		# for get_type_link in get_tag_div:
		# 	for get_link_restaurant in get_type_link.css("a::attr(href)").extract():
		# 		yield scrapy.Request(url=get_link_restaurant+"/dishlist", callback=self.get_menu_data)
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


	# --- get list menu by restaurant ---
	def get_menu_data(self, response):
		get_menu_url = response.request.url
		name_restaurant = response.css("div.list-desc")
		for get_data in name_restaurant:
			# print ("Link = ",get_data.css("a::attr(href)").extract())
			urls_menu = get_data.css("a::attr(href)").extract()
			for loop_url_menu in urls_menu:
				if loop_url_menu:
					yield scrapy.Request(url="http://www.dianping.com/"+loop_url_menu, callback=self._get_menu_data)
					
if __name__ == "__main__":
	process = CrawlerProcess(get_project_settings())
	process.crawl('dianping_spider')
	process.start()		