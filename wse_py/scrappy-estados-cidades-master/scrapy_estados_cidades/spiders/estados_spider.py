
import scrapy
from scrapy_estados_cidades.items import Estado

class EstadosSpider(scrapy.Spider):
	name = "estados_spider"
	allowed_domains = ["http://www.cidades.ibge.gov.br"]
	start_urls = [
		"http://www.cidades.ibge.gov.br/xtras/home.php"
	]

	def parse(self, response):
		for item in response.xpath('//*[@id="menu_ufs"]').xpath('//li'):
			_id = item.xpath('@id').extract()
			if len(_id) > 0 and 'uf' in item.xpath('@id').extract()[0]:
				estado = Estado()
				estado['sigla'] = item.xpath('a').xpath('text()').extract()[0]
				estado['nome'] = item.xpath('a').xpath('@title').extract()[0]
				estado['cod_uf'] = item.xpath('@id').extract()[0][2:]
				yield estado
			