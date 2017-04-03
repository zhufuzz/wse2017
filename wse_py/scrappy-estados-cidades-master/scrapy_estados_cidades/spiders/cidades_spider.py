import scrapy
from scrapy_estados_cidades.items import Cidade

class CidadesSpider(scrapy.Spider):
	name = "cidades_spider"
	allowed_domains = ["www.cidades.ibge.gov.br"]
	start_urls = [
		"http://www.cidades.ibge.gov.br/xtras/home.php",
		""
	]

	def parse(self, response):
		for item in response.xpath('//*[@id="menu_ufs"]').xpath('//li'):
			_id = item.xpath('@id').extract()
			if len(_id) > 0 and 'uf' in item.xpath('@id').extract()[0]:
				url = item.xpath('a').xpath('@href').extract()[0]
				full_url = response.urljoin(url)
				yield scrapy.Request(full_url, callback=self.parse_cidade)

	def parse_cidade(self, response):
	 	cod_uf = response._url.split("&")[1].split("=")[1]
	 	for item in response.xpath('//*[@id="breadcrumb"]/span').xpath('//li'):
	 		_url = item.xpath('a').xpath('@href').extract()
	 		li_id = item.xpath('@id').extract()
	 		if len(_url) > 0 and 'codmun' in _url[0] and len(li_id) > 0 and 'm' in li_id[0]:
	 			_url = _url[0]
	 			cidade = Cidade()
		 		cidade['cod'] = _url.split("&")[1].split("=")[1]
		 		cidade['cod_uf'] = cod_uf
		 		cidade['nome'] = item.xpath('a').xpath('text()').extract()[0]
		 		yield cidade
