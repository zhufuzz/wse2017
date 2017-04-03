# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
''''''
if os.environ.get('HTTP_PROXY'):
  HTTP_PROXY = os.environ.get('HTTP_PROXY')
else:
  raise Exception("Oh, no proxy?!")


BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'example.scrapy_util.downloadermiddleware.rotate_useragent.RotateUserAgentMiddleware': 500,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'example.scrapy_util.downloadermiddleware.http_proxy.HttpProxyMiddleware': 751 
}

ITEM_PIPELINES = {
  'example.pipelines.DuplicatesPipeline': 100
}

DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 25 # number of tor instances?!

AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 60

RETRY_ENABLED = True
RETRY_TIMES = 2 # + initial request
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 429, 421, 423, 408, 404]


LOG_LEVEL = 'DEBUG'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'example (+http://www.yourdomain.com)'
