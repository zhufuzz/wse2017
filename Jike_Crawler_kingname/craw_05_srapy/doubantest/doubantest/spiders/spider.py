# -*- coding: utf-8 -*-
# from scrapy.contrib.spiders import CrawlSpider
from scrapy.spiders import CrawlSpider


class Douban(CrawlSpider):
    name = "doubanTest"
    start_urls = ['http://movie.douban.com/top250'
    ]
    def parse(self,response):
        print response.body
        #print response.url
        #print "ddd"
        #a = response.url
        #b = 1

#