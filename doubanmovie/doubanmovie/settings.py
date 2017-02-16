# -*- coding: utf-8 -*-

# Scrapy settings for doubanmovie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'doubanmovie'

SPIDER_MODULES = ['doubanmovie.spiders']
NEWSPIDER_MODULE = 'doubanmovie.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
ITEM_PIPELINES = {
    'doubanmovie.pipelines.DoubanmoviePipeline': 300,
    #'novelspider.pipelines.JsonWriterPipeline': 800,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanmovie (+http://www.yourdomain.com)'
#FEED_URI = u'file:///Users/tzh/PycharmProjects/wse2017/doubanmovie/douban.csv'
#FEED_FORMAT = 'CSV'
