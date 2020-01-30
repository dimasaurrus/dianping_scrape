# encoding: utf-8
import scrapy
import re
import json
import nltk
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import random
from lxml.html import fromstring
from collections import defaultdict
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http.cookies import CookieJar
from dianping_scrape.items import RestaurantItem
from scrapy.selector import Selector

from tbselenium.tbdriver import TorBrowserDriver
from os.path import dirname, join, realpath, getsize

from selenium.webdriver.common.by import By

# headerInfo = {'content-type': 'application/json' }

list_restaurant_by_city = {}
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"

	# handle_httpstatus_list = [301, 302]
	def get_proxies(self,empty):
		url = 'https://free-proxy-list.net/'
		response = requests.get(url)
		parser = fromstring(response.text)
		list_ip = []
		proxies = set()
		for i in parser.xpath('//tbody/tr')[:100]:
			if i.xpath('.//td[7][contains(text(),"yes")]'):
				#Grabbing IP and corresponding PORT
				proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
				proxies.add(proxy)
		for loop_proxies in proxies:
			list_ip.append(loop_proxies)

		return list_ip

	# --- webdrive for selenium ---
	def __init__(self):
		empty=""
		self.browser = webdriver.PhantomJS()
		self.tbb_dir = "/home/dimdoms/Downloads/tor-browser-linux64-9.0.4_en-US/tor-browser_en-US/"
		self.session = {'X-Crawlera-Session': 'create'}
		self.ip = self.get_proxies(empty)
		self.list_user_agent = [
			'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]
		# self.browser = TorBrowserDriver(self.tbb_dir, tbb_logfile_path='test.log')

	# --- url list of city ---
	def start_requests(self):
		start_urls = [
			"http://www.dianping.com/citylist"
		]
		proxy = random.choice(self.ip)
		user_agent = random.choice(self.list_user_agent)
		req= scrapy.Request(
			url=start_urls[0], 
			callback=self.get_all_city,
			headers={"User-Agent": user_agent},
			meta={
				"proxy":"http://"+proxy
			},
		)
		yield req

	# --- get link food by city ---
	def get_all_city(self, response):
		get_city = response.css("div.findHeight a.onecity::attr(href)").extract()

		proxy = random.choice(self.ip)
		user_agent = random.choice(self.list_user_agent)

		for loop_city in get_city:
			url_by_city = loop_city.replace("//", "http://")
			yield scrapy.Request(
				url=url_by_city+"/food",
				headers={"User-Agent": user_agent},
				meta={
					"proxy":"http://"+proxy
				},			
				callback=self.get_link_restaurant,
			)

	# --- get list restaurant by city ---
	def get_link_restaurant(self, response):
		# for get_review_restaurant in response.css("div.popular-nav ul.Fix a::attr(title)").extract():
		proxy = random.choice(self.ip)
		user_agent = random.choice(self.list_user_agent)

		if response.css("div.popular-nav ul.Fix"):
			for loop_restaurant in response.css("div.popular-nav ul.Fix"):
				for get_review_restaurant in loop_restaurant.css("a").extract():
					soup = BeautifulSoup(get_review_restaurant, features='html.parser')
					for a in soup.find_all('a'):
						try:
							if a['title'] == "评价餐厅":
								yield scrapy.Request(
									url="http://www.dianping.com"+a['href'] ,
									headers={"User-Agent": user_agent},
									meta={
										"proxy":"http://"+proxy
									},										
									callback=self.get_data_restaurant)
						except:
							pass
		else:
			pass


	# --- process json restaurant
	def _process_value_restaurant_json(self, get_json_value):
		self.browser.get(get_json_value)
		gets = json.loads(self.browser.find_element_by_tag_name('body').text)
		return gets

	# --- get link restaurant ---
	def get_data_restaurant(self, response):
		get_url = response.request.url	
		# self.driver.load_url(get_url, wait_for_page_body=True)
		url_restaurant = ""
		vals_json = []

		self.browser.get(get_url)
		list_link = get_url.split("/")
		prefix = "http://www.dianping.com/mylist/ajax/"
		middle = "shoprank?"
		get_rank_id = list_link[-1].split("pcChannelRankingV2?")
		rank_id = get_rank_id[-1]
		next_url = prefix+middle+rank_id

		get_json_value = next_url
		proxy = random.choice(self.ip)
		user_agent = random.choice(self.list_user_agent)

		res_retaurant_value = self._process_value_restaurant_json(get_json_value)
		for key, value in res_retaurant_value.items():
			if key == "shopBeans":
				for values in value:
					url_restaurant = "http://www.dianping.com/shop/"+values["shopId"]
					vals_json.append(values)

		yield scrapy.Request(
			url=url_restaurant+"/dishlist",
			headers={"User-Agent": user_agent},
			meta={
				"data_rest":vals_json,
				"proxy":"http://"+proxy
			}, 
			callback=self.get_list_menu_restaurant
		)

		# html = self.browser.page_source
		# soup = BeautifulSoup(html, features='html.parser')
		# get_table = soup.find("table")
		# try:
		# for get_link_and_name_restaurant in get_table.select(".J_shopName"):
		# 	get_link = get_link_and_name_restaurant.get("href")
		# 	yield scrapy.Request(url=get_link+"/dishlist", callback=self.get_list_menu_restaurant)
		# except AttributeError:
		# 	pass
		# ====================================
		# print (get_table)
		# print ("=-=-=-=-=-=-=-= ")
		# for get_link_and_name_restaurant in get_table.select(".J_shopName"):
		# 	get_link = get_link_and_name_restaurant.get("href")
		# 	yield scrapy.Request(url=get_link+"/dishlist", callback=self.get_list_menu_restaurant)
		# except AttributeError:
		# 	pass


	# --- get list menu by restaurant ---
	def get_list_menu_restaurant(self, response):	
		proxy = random.choice(self.ip)
		user_agent = random.choice(self.list_user_agent)

		json_restaurant = response.meta["data_rest"]
		name_restaurant = response.css("div.list-desc")
		for get_data in name_restaurant:
			# print ("Link = ",get_data.css("a::attr(href)").extract())
			urls_menu = get_data.css("a::attr(href)").extract()
			for loop_url_menu in urls_menu:
				if loop_url_menu:					
					yield scrapy.Request(
						url="http://www.dianping.com"+loop_url_menu, 
						headers={"User-Agent": user_agent},
						meta = {
							'info_json_rest':json_restaurant,
							'dont_redirect': True,
							"proxy":"http://"+proxy,
							'handle_httpstatus_list': [302]
						}, callback=self._get_menu_data
					)

	# --- get menu by restaurant ---
	def _get_menu_data(self, response):
		get_menu_url = response.request.url
		name_city = response.css("a.J-city span::text").extract()
		restaurant_name = response.meta["info_json_rest"]["shopName"]
		restaurant_category = response.meta["info_json_rest"]["mainCategoryName"]
		restaurant_flavor = response.meta["info_json_rest"]["refinedScore1"]
		restaurant_surroundings = response.meta["info_json_rest"]["refinedScore2"]
		restaurant_service = response.meta["info_json_rest"]["refinedScore3"]
		average_price = response.meta["info_json_rest"]["avgPrice"]

		check_header = response.css("div.dish-crumb")
		try:
			name_food = check_header.css("li a::text").extract()[-1]
		except:
			name_food = check_header.css(" div.dish-name::text").extract()
		food_price = response.css("div.dish-price span::text").extract()

		data = {
				"city":name_city,
				"name retaurant":restaurant_name,
				"category restaurant":restaurant_category,
				"flavor restaurant":restaurant_flavor,
				"surrounding restaurant":restaurant_surroundings,
				"service restaurant":restaurant_service,
				"avergae price":average_price,
				"name food":name_food,
				"food price":food_price,
		}

		print (json.dumps(data,  ensure_ascii=False, indent=4, sort_keys=True).encode('utf8').decode())
		print ("=--0-0-0-0-0-0-0-0--0-0-0=-=-=-")
		print ()
		
		# print (info_restaurant.css("div.bottom-other-info div.ranks").extract())
		# print ("=-=-=-=-=-==-")		
if __name__ == "__main__":
	process = CrawlerProcess(get_project_settings())
	process.crawl('dianping_spider')
	process.start()		