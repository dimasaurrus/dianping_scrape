# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dianping_scrape.items import RestaurantItem
from dianping_scrape.spiders.dianping_spider import DiangpingScrape

get_start_requests = DiangpingScrape()
class DianpingScrapePipeline(object):
	GlobalPipelineTerminator = True
	def process_item(self, item, spider):
		if isinstance(item, RestaurantItem):
			return item
