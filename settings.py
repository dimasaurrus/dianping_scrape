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
LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
	# 'Cookie':'s_ViewType=10; _lxsdk_s=16eb7c37081-08b-750-06a%7C%7C200; _lxsdk_cuid=16eb8d09cf5c8-05ca75fa4b8f66-14291003-100200-16eb8d09cf5c8; _lxsdk=16eb8d09cf5c8-05ca75fa4b8f66-14291003-100200-16eb8d09cf5c8; _hc.v=8f832efa-3775-aeec-1189-37c6d815ecb0.1575058712'
	# 'Cookie':'ALF=1573490222; _T_WM=148616430989eb5a607186e5ccc1bd5a4754b18b318; SCF=AlnIW_LpGKigwbo6ysyWWwVvTa_owlI2qJO_J1CxkMPEGosrBTKlnFR2fkvt82OUSt8ALZaDaUYGDQ9K0TtOAK8.; SUB=_2A25wpnFhDeRhGeFN6loW9CrPyDiIHXVQaR8prDV6PUJbktBeLRahkW1NQEqapQmLSHVEFcFyeIkn1OBaYewoa96T; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFEx4XGa4r.ozPRKdw4_Wmx5JpX5K-hUgL.FoM0eKnNShB0e0B2dJLoIpRLxK-LB-BL1KBLxK-LBKBLB-zLxK-LB-BL1K5peo-t; SUHB=0TPVAlkzF8-YRN; SSOLoginState=1570898225; MLOGIN=1; _T_WL=1'
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
	'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 500,
	# 'dianping_scrape.middlewares.RotateUserAgentMiddleware': 543,
	# 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
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

# ==============================
# RETRY_ENABLED = True
# RETRY_TIMES = 3
# RETRY_HTTP_CODES =  [500, 502, 503, 504, 408, 302]
# DOWNLOAD_TIMEOUT = 180
# DOWNLOAD_MAXSIZE = 1073741824