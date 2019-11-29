# -*- coding: utf-8 -*-

# Scrapy settings for dianping_scrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dianping_scrape'

SPIDER_MODULES = ['dianping_scrape.spiders']
NEWSPIDER_MODULE = 'dianping_scrape.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'dianping_scrape (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'
LOG_ENABLED = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS = {
	# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
	'Cookie':'s_ViewType=10; _lxsdk_s=16eb7c37081-08b-750-06a%7C%7C200; _lxsdk_cuid=16eb8d09cf5c8-05ca75fa4b8f66-14291003-100200-16eb8d09cf5c8; _lxsdk=16eb8d09cf5c8-05ca75fa4b8f66-14291003-100200-16eb8d09cf5c8; _hc.v=8f832efa-3775-aeec-1189-37c6d815ecb0.1575058712'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'dianping_scrape.middlewares.DianpingScrapeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
	'dianping_scrape.middlewares.DianpingScrapeDownloaderMiddleware': 543,
	# 'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
	# 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
	# 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
	# 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
	# 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
	# 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
	# 'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
	# 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
	# 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
	# 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
	# 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
	# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
	# 'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
	# 'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
	'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
	'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
	'sina.pipelines2.SpiderStatusMiddleware':None
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'dianping_scrape.pipelines.DianpingScrapePipeline': 300,
   # 'dianping_scrape.downloadermiddlewares.cookies.CookiesMiddleware': 700,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPERROR_ALLOWED_CODES = [404]