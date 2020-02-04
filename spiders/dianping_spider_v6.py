# encoding: utf-8
import scrapy
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

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

# headerInfo = {'content-type': 'application/json' }

list_restaurant_by_city = {}
class DiangpingScrape(scrapy.Spider):
	name = "dianping_spider"

	# --- webdrive for selenium ---
	def __init__(self):
		empty=""
		self.browser = webdriver.PhantomJS()
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.tbb_dir = "/home/dimdoms/Downloads/tor-browser-linux64-9.0.4_en-US/tor-browser_en-US/"
		self.session = {'X-Crawlera-Session': 'create'}
		# self.tbbrowser = TorBrowserDriver(self.tbb_dir, tbb_logfile_path='test.log')
		self.list_city = [
			["上海","fce2e3a36450422b7fad3f2b90370efd71862f838d1255ea693b953b1d49c7c0"],
			["北京","d5036cf54fcb57e9dceb9fefe3917fff71862f838d1255ea693b953b1d49c7c0"],
			["广州","e749e3e04032ee6b165fbea6fe2dafab71862f838d1255ea693b953b1d49c7c0"],
			["深圳","e049aa251858f43d095fc4c61d62a9ec71862f838d1255ea693b953b1d49c7c0"],
			["天津","2e5d0080237ff3c8f5b5d3f315c7c4a508e25c702ab1b810071e8e2c39502be1"],
			["杭州","91621282e559e9fc9c5b3e816cb1619c71862f838d1255ea693b953b1d49c7c0"],
			["南京","d6339a01dbd98141f8e684e1ad8af5c871862f838d1255ea693b953b1d49c7c0"],
			["苏州","536e0e568df850d1e6ba74b0cf72e19771862f838d1255ea693b953b1d49c7c0"],
			["成都","c950bc35ad04316c76e89bf2dc86bfe071862f838d1255ea693b953b1d49c7c0"],
			["武汉","d96a24c312ed7b96fcc0cedd6c08f68c08e25c702ab1b810071e8e2c39502be1"],
			["重庆","6229984ceb373efb8fd1beec7eb4dcfd71862f838d1255ea693b953b1d49c7c0"],
			["西安","ad66274c7f5f8d27ffd7f6b39ec447b608e25c702ab1b810071e8e2c39502be1"]
		]

	# -- selenium_dragn_drop
	def _test_dragelement(self, url_verify):
		# driver = self.driver
		self.driver.maximize_window()
		# self.driver.get('https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=07454363df3644ec8e99ec2836784ae0&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshop%252F110714928%252Fdishlist&theme=dianping')
		self.driver.get(url_verify)
 
		# self.driver.switch_to.frame(0)
		self.driver.switch_to.default_content()
		wait = WebDriverWait(self.driver,30)

		tags1 = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.boxStatic')))
		tags2 = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.moveingBar')))
		# tags1 = self.driver.find_element_by_css_selector("#boxStatic")
		# tags2 = self.driver.find_element_by_css_selector("#moveingBar")
		self.driver.implicitly_wait(100)
		action = ActionChains(self.driver)
 
		#move element by x,y coordinates on the screen
		action.drag_and_drop_by_offset(tags1, 197, 0).perform()
		# action.drag_and_drop_by_offset(tags2, 208, 0).perform()
		# self.driver.implicitly_wait(100)
		# time.sleep(10)
		# self.driver.refresh()
		# yield Request.scrapy(url=real_url, callback=self.get_data_restaurant)


	# --- url list of city ---
	def start_requests(self):
		start_urls = [
			"http://www.dianping.com/shoplist/shopRank/pcChannelRankingV2?rankId="
		]
		# proxy = random.choice(self.ip)
		# user_agent = random.choice(self.list_user_agent)

		# for i, url in enumerate(self.list_city):
		for url in self.list_city:
			req= scrapy.Request(
				url=start_urls[0]+url[1], 
				callback=self.get_data_restaurant,
			)
			yield req


	# --- process json restaurant
	def _process_value_restaurant_json(self, get_json_value):
		self.browser.get(get_json_value)
		gets = json.loads(self.browser.find_element_by_tag_name('body').text)
		return gets

	# --- get link restaurant ---
	def get_data_restaurant(self, response):
		print ("MASUK")
		print ("=-=-=-=-=-")
		if "verify" in response.request.url:
			url_verify = response.request.url
			self._test_dragelement(url_verify)
		else:		
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
			# proxy = random.choice(self.ip)

			res_retaurant_value = self._process_value_restaurant_json(get_json_value)
			for key, value in res_retaurant_value.items():
				if key == "shopBeans":
					for values in value:
						url_restaurant = "http://www.dianping.com/shop/"+values["shopId"]
						vals_json.append(values)

			res = scrapy.Request(
				url=url_restaurant+"/dishlist",
				meta={
					"data_rest":vals_json,
					"real_url":url_restaurant+"/dishlist"
					# "proxy":"https://"+proxy,
					# "handle_httpstatus_list": [302]
				}, 
				callback=self.get_list_menu_restaurant
			)
			# res.meta['dont_redirect'] = True
			print (res)
			print ("===============")
			yield res


	# --- get list menu by restaurant ---
	def get_list_menu_restaurant(self, response):
		print ("MASUK 2")
		print (response.request.url)
		print ("=-=-=-=-=-")
		if "verify" in response.request.url:
			url_verify = response.request.url
			real_url = response.meta["real_url"]
			print (url_verify)
			print ("-TTTTTTTTTTT")
			# self._test_dragelement(url_verify)
		else:
			# proxy = random.choice(self.ip)
			# user_agent = random.choice(self.list_user_agent)
			json_restaurant = response.meta["data_rest"]
			name_restaurant = response.css("div.list-desc")

			for get_data in name_restaurant:
				urls_menu = get_data.css("a::attr(href)").extract()
				for loop_url_menu in urls_menu:
					if loop_url_menu:
						time.sleep(3)		
						res = scrapy.Request(
							url="http://www.dianping.com"+loop_url_menu, 
							meta = {
								'info_json_rest':json_restaurant,
							}, 
							callback=self._get_menu_data
						)
						time.sleep(5)
						yield res

	# --- get menu by restaurant ---
	def _get_menu_data(self, response):
		# print (response.meta["info_json_rest"])
		print ("----------------")
		print (response.request.url)
		print (response.status)
		print ("||||||||||||||||")
		res = []
		get_menu_url = response.request.url
		for loop_get_json in response.meta["info_json_rest"]:
			name_city = response.css("a.J-city span::text").extract()
			if not name_city:
				name_city = response.css("div.food-conf div.clearfix a.J-city::text").extract()
			restaurant_name =loop_get_json["shopName"]
			restaurant_category =loop_get_json["mainCategoryName"]
			restaurant_flavor =loop_get_json["refinedScore1"]
			restaurant_surroundings =loop_get_json["refinedScore2"]
			restaurant_service =loop_get_json["refinedScore3"]
			average_price =loop_get_json["avgPrice"]

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
			res.append(data)

		print (json.dumps(data,  ensure_ascii=False, indent=4, sort_keys=True).encode('utf8').decode())
		print ("=--0-0-0-0-0-0-0-0--0-0-0=-=-=-")
		print ()

		with open('outputfile2.json', 'w', encoding='utf-8') as dianping_data:
			json.dump(res, dianping_data,  ensure_ascii=False, indent=2)		
		
		# print (info_restaurant.css("div.bottom-other-info div.ranks").extract())
		# print ("=-=-=-=-=-==-")		
if __name__ == "__main__":
	process = CrawlerProcess(get_project_settings())
	process.crawl('dianping_spider')
	process.start()		