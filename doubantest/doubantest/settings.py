# -*- coding: utf-8 -*-

# Scrapy settings for doubantest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'doubantest'

SPIDER_MODULES = ['doubantest.spiders']
NEWSPIDER_MODULE = 'doubantest.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubantest (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'doubantest.pipelines.DoubantestPipeline': 300,
    #'novelspider.pipelines.JsonWriterPipeline': 800,
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanmovie (+http://www.yourdomain.com)'
