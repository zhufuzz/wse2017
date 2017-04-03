# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyEstadosCidadesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Estado(scrapy.Item):
	cod = scrapy.Field()
	nome = scrapy.Field()
	sigla = scrapy.Field()

class Cidade(scrapy.Item):
	cod = scrapy.Field()
	cod_uf = scrapy.Field()
	nome = scrapy.Field()
	
				
