import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoztools.net"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

#    '''def parse(self, response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)'''

    def parse(self, response):
		for sel in response.xpath('//ul/li'):
			#title = sel.xpath('a/text()').extract()
			link = sel.xpath('a/@href').extract()
			#desc = sel.xpath('text()').extract()
			#print title
			print link
			#print desc