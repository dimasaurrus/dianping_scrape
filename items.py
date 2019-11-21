# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class RestaurantItem(Item):
	_id = Field()
	city = Field()
	restaurant_url = Field() 
	restaurant_name = Field()


# class DianpingScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
