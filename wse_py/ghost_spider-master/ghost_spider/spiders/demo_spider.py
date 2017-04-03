# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ghost_spider.items import HotelItem
from ghost_spider import helper


class DemoSpider(Spider):
  name = "demo"
  allowed_domains = ["localhost"]
  target_base_url = "file://localhost/Users/jctt/Developer/crawler/ghost_spider/samples/hotels"
  start_urls = [
      "file://localhost/Users/jctt/Developer/crawler/ghost_spider/samples/hotels/target_list_of_places.html"
  ]

  def parse(self, response):
    # print current area
    count = 0
    sel = Selector(response)
    links = sel.xpath(helper.SEL_LIST_PLACES).extract()
    if links:
      for link in links:
        count += 1
        area_name = helper.place_sel_name.findall(link)[0]
        area_link = self.target_base_url + helper.place_sel_link.findall(link)[0]
        request = Request(area_link, callback=self.parse, errback=self.parse_err)
        request.meta['area_name'] = area_name
        request.meta['area_level'] = long(response.meta.get('area_level') or 1) + 1
        yield request
    else:
      # possible last level
      links = sel.xpath(helper.SEL_LIST_PLACES_LAST).extract()
      if links:
        for link in links:
          area_name = helper.place_sel_name_last.findall(link)[0]
          area_link = self.target_base_url + helper.place_sel_link_last.findall(link)[0]
          # don't scrap the page if it was crawled
          # if PlaceHs.check_by_url(area_link):
          #  continue
          request = Request(area_link, callback=self.parse_place, errback=self.parse_err)
          request.meta['area_name'] = area_name
          request.meta['area_level'] = long(response.meta.get('area_level') or 1) + 1
          yield request
          count += 1
    if response.meta.get('area_name'):
      print "%s> %s total(%s)" % ("-----" * response.meta.get('area_level') or 1, response.meta['area_name'], count)

  def parse_err(self, response):
    pass

  def parse_place(self, response):
    if response.meta.get('area_name'):
      print "%s> %s" % ("-----" * response.meta.get('area_level') or 1, response.meta['area_name'])
    sel = Selector(response)
    item = HotelItem()
    item['page_url'] = response.url
    item['page_breadcrumbs'] = sel.xpath(helper.SEL_BREADCRUMBS).extract()
    item['name'] = sel.xpath(helper.SEL_HOTEL_NAME).extract()
    item['phone'] = sel.xpath(helper.SEL_PHONE_NUMBER).extract()
    item['address_area_name'] = sel.xpath(helper.SEL_AREA_NAME).extract()
    item['address_street'] = sel.xpath(helper.SEL_AREA_STREET).extract()
    item['address_locality'] = sel.xpath(helper.SEL_AREA_LOCALITY).extract()
    item['address_region'] = sel.xpath(helper.SEL_AREA_REGION).extract()
    item['address_zip'] = sel.xpath(helper.SEL_AREA_ZIP).extract()
    item['amenity'] = sel.xpath(helper.SEL_AMENITIES).extract()
    item['rating'] = sel.xpath(helper.SEL_RATING).re(r'(.*)\s*of 5')
    item['popularity'] = sel.xpath(helper.SEL_PERCENT).re(r'(.*)\s*%')
    item['page_body'] = helper.get_body(sel)
    links = {
      'es': sel.xpath(helper.SEL_SPANISH_PAGE).extract(),
      'ja': sel.xpath(helper.SEL_JAPANESE_PAGE).extract(),
      'zh': sel.xpath(helper.SEL_CHINESE_PAGE).extract()
    }

    for name, link in links.iteritems():
      links[name] = link[0]
    request = Request(links['ja'], callback=self.parse_local_page)
    request.meta['remain'] = ['ja', 'es', 'zh']
    request.meta['links'] = links
    request.meta['item'] = item
    return request

  def parse_local_page(self, response):
    current = response.meta['remain'][0]
    remain = response.meta['remain'][1:]
    sel = Selector(response)
    item = response.meta['item']
    item['name_%s' % current] = sel.xpath(helper.SEL_HOTEL_NAME).extract()
    item['address_area_name_%s' % current] = sel.xpath(helper.SEL_AREA_NAME).extract()
    item['address_street_%s' % current] = sel.xpath(helper.SEL_AREA_STREET).extract()
    item['address_locality_%s' % current] = sel.xpath(helper.SEL_AREA_LOCALITY).extract()
    item['address_region_%s' % current] = sel.xpath(helper.SEL_AREA_REGION).extract()
    item['address_zip_%s' % current] = sel.xpath(helper.SEL_AREA_ZIP).extract()
    item['amenity_%s' % current] = sel.xpath(helper.SEL_AMENITIES).extract()
    item['page_body_%s' % current] = helper.get_body(sel)
    if remain and len(remain) > 0:
      from ghost_spider.settings import REQUEST_HEADERS
      next_lang = remain[0]
      request = Request(response.meta['links'][next_lang], headers=REQUEST_HEADERS[next_lang], callback=self.parse_local_page, errback=self.parse_err)
      request.meta['remain'] = remain
      request.meta['links'] = response.meta['links']
      request.meta['item'] = item
      return request
    return item
