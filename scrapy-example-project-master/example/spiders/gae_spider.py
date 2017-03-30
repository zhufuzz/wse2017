from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import log
import time, random
from example.items import PageItem

class GaeSpider(Spider):
    name = "gae"
    start_urls = []

    def __init__(self, **kwargs):
        # super(GaeSpider, self).__init__(self, **kwargs)
        job_id = "4"
        requests = 1000
        for i in range(1, requests):
            randomstr = str(int(round(time.time() * 1000))) + str(random.randint(1, 999))
            url = "http://scrapy-bench-server-1.appspot.com/foobar?job_id=%s&body_length=76800&randomstr=%s" % (job_id, randomstr)
            self.start_urls.append(url)

    def parse(self, response):
        # log.msg("%s" % response.url, level=log.INFO)
        pass
        
