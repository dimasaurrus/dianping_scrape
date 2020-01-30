# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import sys
from scrapy import Item, Field
from importlib import reload
import json

class RestaurantItem(Item):
	_id = Field()
	city = Field()
	restaurant_url = Field() 
	link_menus = Field()
	name_restaurant = Field()
	region = Field()
	taste = Field()

# ===========================================

class TestItem (Item):
	# restaurant name
	shop_name = Field()
	# home map
	shop_img = Field()
	# shop star
	shop_star = Field()
	# shop reviewer 
	shop_evaluation = Field()
	# per capita price
	shop_price = Field()
	# Cuisines
	shop_type = Field()
	# address 1
	shop_address1 = Field()
	# address
	shop_address2 = Field()
	# recommended dishes 1
	shop_food1 = Field()
	# recommended Dish 2
	shop_food2 = Field()
	# recommended dish 3
	shop_food3 = Field()
	# taste score
	shop_sweet = Field()
	# environment score
	shop_environment = Field()
	# service score
	shop_server = Field()

class TestPipeline(object):
	"""
		Function: save item data
	"""
	def __init__(self):
	# Open file
		self.filename = open("shuiguoshengxian.json", "w")
		def process_item(self, item, spider ):
			# Convert each item obtained to json format
			text = json.dumps(dict(item), ensure_ascii = False)+",\n"
			self.filename.write(text)
			return item

		def close_spider(self, spider ):
			# close the fil
			self.filename.close()

# ====================================================

class ShopItem(Item):
	name = Field()
	link = Field()
	lng = Field()
	lat = Field()

class DishItem(Item):
	name = Field()
	link = Field()