# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_APP project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# 一些不便于上传GitHub的信息放在同步录下的 config.py 文件里，对于提示缺少的值，建立相应的文件自己写入即可
from scrapy_APP.config import *
# For this project

import os
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
PROJECT_ROOT = os.path.dirname(__file__)
DRIVER_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.path.pardir, 'driver'))
DRIVER_NAME = "chromedriver.exe"
DRIVER_FILE = os.path.abspath(os.path.join(DRIVER_DIR, DRIVER_NAME))

# For Simple Desktop Spider Only
IMAGES_URLS_FIELD = 'src'
IMAGES_STORE = os.path.abspath(os.path.join(PROJECT_ROOT, 'image_downloaded', 'simple_desktop'))


# For Scrapy-Redis
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#Redis config
try:
    REDIS_URL = redis_url
except NameError:
    REDIS_URL = "redis://127.0.0.1"

# default
BOT_NAME = 'scrapy_APP'

SPIDER_MODULES = ['scrapy_APP.spiders']
NEWSPIDER_MODULE = 'scrapy_APP.spiders'

# 是否允许暂停，即程序意外宕机重启后从上次意外退出的地方重新爬取
SCHEDULER_PERSIST = True

#Redis服务器地址，代码拷贝到其他服务器后，爬取的数据将保存到如下地址的redis服务器中
REDIS_HOST="47.116.17.149"

#Redis服务器端口
REDIS_PORT=6379

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_APP (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

LOG_LEVEL='ERROR'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_APP.middlewares.AppSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'scrapy_APP.middlewares.AppDownloaderMiddleware': 543
    'scrapy_APP.middlewares.WangyiproDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy_redis.pipelines.RedisPipeline': 300
    #'scrapy.pipelines.images.ImagesPipeline': 300
    'scrapy_APP.pipelines.WangyiproPipeline':300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
