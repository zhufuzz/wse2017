# -*- coding: utf-8 -*-

import urllib
import re


class AirportSelectors(object):
  """List of selectors for Airports."""
  LIST_AIRPORTS = '//div[contains(@class, "inner")]/table/tr/td[3]/a/@href'
  NAME = '//div[contains(@class, "box-main")]//div[contains(@class, "basic_info_title clear")]/h2/a/text()'
  NAME_ENG = '//div[contains(@class, "box-main")]//div[contains(@class, "basic_info_title clear")]/h2/a/span/text()'
  AREA_INFO = u'//div[contains(@class, "info_ex")]//dt[contains(., "%s")]/following-sibling::dd/a/text()'
  AIRPORT_INFO = u'//div[contains(@class, "info_ex")]//dt[contains(., "%s")]/following-sibling::dd/text()'

  @classmethod
  def get_area_info(cls, sel):
    raw_data = sel.xpath(cls.AREA_INFO % u'都市').extract()
    area = country = ''
    if raw_data and len(raw_data) >= 2:
      area = raw_data[0].strip()
      country = raw_data[1].strip()
    return area, country

  @classmethod
  def get_airport_info(cls, sel):
    raw_data = sel.xpath(cls.AIRPORT_INFO % u'コード').extract()
    codes = raw_data[0].split('|')
    code = code2 = ''
    if codes and len(codes) >= 2:
      code = codes[0].split(':')[1].strip()
      code2 = codes[1].split(':')[1].strip()
    return code, code2


class SalonSelectors(object):
  """List of selectors for Salons."""
  LIST_SALONS = '//div[contains(@class, "uWrap")]/div[contains(@class, "LSaj")]/div[contains(@class, "item")]//h3[contains(@class, "ttl")]/a/@href'
  LIST_TOTAL = '//div[@id="Sf"]/div/p/span[contains(@class, "bo")]/text()'
  NEXT_URL = '//link[@rel="next"]/@href'
  CANONICAL_URL = '//link[@rel="canonical"]/@href'

  NAME = '//div[contains(@class, "title")]//p[contains(@class, "poiTtl")]/a/text()'
  NAME_KATA = '//div[contains(@class, "title")]/div[contains(@class, "ruby")]/text()'
  ADDRESS = '//div[contains(@class, "access")]/p[contains(@class, "address")]/text()'
  ROUTES = '//div[contains(@class, "access")]/p[contains(@class, "route")]/text()'

  SEL_META = '//head/meta'
  SEL_INFO = '//div[@id="outline"]/ul'
  SEL_START = '//div[@id="outline"]/ul'
  SEL_TITLE = '//div[contains(@class, "title")]'
  SEL_BREADCRUMBS = '//div[@id="sHeader"]/div[contains(@class, "link")]/p[contains(@class, "fl")]/a/text()'

  GENERAL_INFO_TABLE = u'//ul[contains(@class, "detailInfo")]//dt[contains(., "%s")]/following-sibling::dd/text()'
  GENERAL_INFO_TABLE_URL = u'//ul[contains(@class, "detailInfo")]//dt[contains(., "%s")]/following-sibling::dd/a/text()'
  GENERAL_INFO_TABLE_CARDS = u'//ul[contains(@class, "detailInfo")]//dt[contains(., "%s")]/following-sibling::dd/span[contains(@class, "logoIcon")]/text()'

  @classmethod
  def get_prefecture_area(cls, sel):
    """extract the most relevant info from the page."""
    data = sel.xpath(cls.SEL_BREADCRUMBS).extract()
    if not data:
      return [], u'', u''
    breadcrumbs = data[1:]
    prefecture = breadcrumbs[0]

    for word in [u'県', u'府', u'都']:
      if prefecture[-1] == word:
        prefecture = prefecture.replace(word, u'')
        break

    area = u''
    for place in breadcrumbs[1:]:
      if u'・' in place:
        continue
      area = place
      break

    if not area and len(breadcrumbs) > 1:
      area = breadcrumbs[1]

    return prefecture, area

  @classmethod
  def get_body(cls, sel):
    """extract the most relevant info from the page."""
    meta = sel.xpath(cls.SEL_META).extract()
    breadcrumbs = sel.xpath(cls.SEL_BREADCRUMBS).extract()
    info = sel.xpath(cls.SEL_INFO).extract()
    title = sel.xpath(cls.SEL_TITLE).extract()
    if breadcrumbs:
      breadcrumbs = breadcrumbs[1:]
    body = {
      'meta': u''.join(meta),
      'breadcrumbs': breadcrumbs,
      'info': info[0] if len(info) else u'',
      'title': title[0] if len(title) else u'',
    }
    return body

  @classmethod
  def get_routes(cls, sel):
    """extract the most relevant info from the page."""
    raw_routes = sel.xpath(cls.ROUTES).extract()
    routes = [_.strip().replace(u'（', u'').replace(u'）', u'') for _ in raw_routes]
    return [route for route in routes if route]

  @classmethod
  def get_phone(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'電話番号').extract()
    return u''.join(raw_data).strip()

  @classmethod
  def get_working_hours(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'営業時間').extract()
    raw_data = [_.strip() for _ in raw_data]
    return u'\n'.join(raw_data)

  @classmethod
  def get_holidays(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'定休日').extract()
    raw_data = [_.strip() for _ in raw_data]
    return u'\n'.join(raw_data)

  @classmethod
  def get_shop_url(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE_URL % u'HP').extract()
    raw_data = [_.strip() for _ in raw_data]
    return u'\n'.join(raw_data)

  @classmethod
  def get_credit_cards(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE_CARDS % u'利用可能カード').extract()
    raw_data = [_.strip() for _ in raw_data]
    ccards = []
    for card in raw_data:
      if card == u'VISA':
        ccards.append(u'VISA')
      elif card == u'MasterCard':
        ccards.append(u'MASTER')
      elif card == u'JCB':
        ccards.append(u'JCB')
      elif card == u'AmericanExpress' or card == 'American Express':
        ccards.append(u'AMERICAN EXPRESS')
      elif card == u'ダイナース' or card == u'DINERS':
        ccards.append(u'DINERS')
      elif card == u'Discover':
        ccards.append(u'DISCOVER')
    comment = u''
    if ccards:
      comment = u'利用可'
    else:
      # check if this shop can accept cards
      features = u''.join(sel.xpath(cls.GENERAL_INFO_TABLE % u'特徴').extract()).strip()
      if u'カード利用' in features:
        comment = u'利用可'
      else:
        comments = u''.join(sel.xpath(cls.GENERAL_INFO_TABLE % u'クレジットカードコメント').extract()).strip().lower()
        avalaible = [u'visa', u'mastercard', u'jcb', u'american express', u'ダイナース', u'その他', 'diner', 'discover']
        for ava in avalaible:
          if ava in comments:
            comment = u'利用可'
            break
        if u'visa' in comments:
          ccards.append(u'VISA')
        if u'master' in comments or u'mastercard' in comments or u'master card' in comments:
          ccards.append(u'MASTER')
        if u'jcb' in comments:
          ccards.append(u'JCB')
        if u'american express' in comments or u'americanexpress' in comments:
          ccards.append(u'AMERICAN EXPRESS')
        if u'ダイナース' in comments or u'diners' in comments:
          ccards.append(u'DINERS')
        if u'discover' in comments:
          ccards.append(u'DISCOVER')
    return comment, ccards

  @classmethod
  def get_seats(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'総席数').extract()
    return u''.join(raw_data).strip()

  @classmethod
  def get_stylist(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'スタイリスト人数').extract()
    return u''.join(raw_data).strip()

  @classmethod
  def get_parking(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'駐車場').extract()
    raw_data = [_.strip() for _ in raw_data]
    return u'\n'.join(raw_data)

  @classmethod
  def get_cut_price(cls, sel):
    raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'カット料金').re(r'\d+')
    if len(raw_data) > 1:
      raw_data = sel.xpath(cls.GENERAL_INFO_TABLE % u'カット料金').extract()
      raw_data = u''.join(raw_data).strip()
    elif len(raw_data) == 1:
      raw_data = u''.join(raw_data).strip()
      try:
        raw_data = int(raw_data)
      except:
        pass
    else:
      raw_data = u''
    return raw_data

  @classmethod
  def get_list_total(cls, sel):
    total = 0
    raw_data = sel.xpath(cls.LIST_TOTAL).extract()
    if len(raw_data) and raw_data[0]:
      str_number = raw_data[0].replace(',', '')
      try:
        total = int(str_number)
      except:
        total = 0
    return total

  @classmethod
  def is_first_page(cls, sel):
    raw_data = sel.xpath(cls.CANONICAL_URL).re(r'&b=\d+')
    if len(raw_data):
      return False
    return True


class LocationHotelSelectors(SalonSelectors):
  LIST_HOTELS = '//div[contains(@class, "uWrap")]/div[contains(@class, "LSaj")]/div[contains(@class, "item")]//h3[contains(@class, "ttl")]/a/@href'
  LIST_TOTAL = '//div[@id="Sf"]/div/p/span[contains(@class, "bo")]/text()'
  NEXT_URL = '//link[@rel="next"]/@href'
  CANONICAL_URL = '//link[@rel="canonical"]/@href'

  NAME = '//div[contains(@class, "title")]//p[contains(@class, "poiTtl")]/a/text()'
  NAME_KATA = '//div[contains(@class, "title")]/div[contains(@class, "ruby")]/text()'
  ADDRESS = '//div[contains(@class, "access")]/p[contains(@class, "address")]/text()'
  ROUTES = '//div[contains(@class, "access")]/p[contains(@class, "route")]/text()'

  SEL_META = '//head/meta'
  SEL_INFO = '//div[@id="outline"]/ul'
  SEL_START = '//div[@id="outline"]/ul'
  SEL_TITLE = '//div[contains(@class, "title")]'
  SEL_BREADCRUMBS = '//div[@id="sHeader"]/div[contains(@class, "link")]/p[contains(@class, "fl")]/a/text()'
  SEL_GENRE_ALL = '//p[contains(@class, "genre")]/a'
  SEL_GENRE = '//p[contains(@class, "genre")]/a/text()'
  SEL_VOTES = '//span[@itemprop="votes"]/a/text()'
  HOTEL_KINDS = [u'ホテル', u'旅館', u'民宿', u'ビジネスホテル', u'ペンション', u'保養所', u'公共の宿', u'貸別荘', u'ラブホテル', u'宿泊施設（その他）']
  REPLACE_HOTEL = {
    u'ホテル': u'ホテル',
    u'旅館': u'旅館',
    u'民宿': u'ペンション・民宿',
    u'ビジネスホテル': u'ビジネスホテル・イン',
    u'ペンション': u'ペンション・民宿',
    u'貸別荘': u'ロッジ・貸別荘',
    u'保養所': u'保養所',
    u'公共の宿': u'公共の宿',
    u'ラブホテル': u'ラブホテル',
    u'宿泊施設（その他）': u'宿泊施設（その他）'
  }

  @classmethod
  def get_prefecture_area(cls, sel):
    """extract the most relevant info from the page."""
    data = sel.xpath(cls.SEL_BREADCRUMBS).extract()
    if not data:
      return [], u'', u''
    breadcrumbs = data[1:]
    prefecture = breadcrumbs[0]

    for word in [u'県', u'府', u'都']:
      if prefecture[-1] == word:
        prefecture = prefecture.replace(word, u'')
        break

    data = sel.xpath(cls.SEL_GENRE).extract()
    area = data[0] if data and len(data) else u''
    if not area and len(breadcrumbs) > 1:
      area = breadcrumbs[1]
    return prefecture, area

  @classmethod
  def get_genre(cls, sel):
    raw_data = sel.xpath(cls.SEL_GENRE).extract()
    # first one is the area, so is not included in the genre list
    return raw_data[1:]

  @classmethod
  def get_working_time(cls, sel):
    checkin = u''.join(sel.xpath(cls.GENERAL_INFO_TABLE % u'チェックイン開始時刻').extract())
    checkout = u''.join(sel.xpath(cls.GENERAL_INFO_TABLE % u'チェックアウト時刻').extract())
    return checkin.strip(), checkout.strip()

  @classmethod
  def get_hotel_type(cls, sel):
    data = (u''.join(sel.xpath(cls.GENERAL_INFO_TABLE % u'宿のタイプ').extract())).strip()
    if data not in cls.HOTEL_KINDS:
      data = u'ホテル'
    data = cls.REPLACE_HOTEL.get(data) or u'ホテル'
    return data

  @classmethod
  def get_body(cls, sel, is_restaurant=False):
    """extract the most relevant info from the page."""
    meta = sel.xpath(cls.SEL_META).extract()
    breadcrumbs = sel.xpath(cls.SEL_BREADCRUMBS).extract()
    info = sel.xpath(cls.SEL_INFO).extract()
    title = sel.xpath(cls.SEL_TITLE).extract()
    if breadcrumbs:
      breadcrumbs = breadcrumbs[1:]
    body = {
      'meta': u''.join(meta),
      'breadcrumbs': breadcrumbs,
      'info': info[0] if len(info) else u'',
      'title': title[0] if len(title) else u'',
    }
    if is_restaurant:
      body['genre'] = sel.xpath(cls.SEL_GENRE_ALL).extract()
    return body

  @classmethod
  def get_votes(cls, sel):
    """extract number of reviews posted for this hotel."""
    vote_raw = sel.xpath(cls.SEL_VOTES).re(r'\d+')
    vote = 0
    try:
      vote = int(vote_raw[0].replace(',', ''))
    except:
      pass
    return vote

  @classmethod
  def get_category(cls, sel):
    raw_data = sel.xpath(cls.CANONICAL_URL).re(r'genrecd=\d+')
    if len(raw_data):
      return raw_data[0].replace('genrecd=', '')
    return ""

  @classmethod
  def get_restaurant_genre(cls, sel):
    """extract number of reviews posted for this hotel."""
    genre_code = [s.replace('genrecd=', '') for s in sel.xpath('//p[contains(@class, "genre")]/a').re(r'genrecd=\d+')]
    genre_str = sel.xpath(cls.SEL_GENRE).extract()
    genre = []
    for k, v in enumerate(genre_code):
      if v == '01':
        # this genre refers to area mostly
        continue
      genre.append(genre_str[k])
    return genre

  @classmethod
  def convert_latte_kind(cls, loco_genre):
    """extract number of reviews posted for this hotel."""
    from ghost_spider.data import RST_KINDS_LATE_MAP
    latte_genre = []
    for genre in loco_genre:
      if genre in RST_KINDS_LATE_MAP:
        latte_genre.append(RST_KINDS_LATE_MAP[genre])
    return latte_genre

# selector for country, prefectures and areas
SEL_LIST_PLACES = '//div[@id="BODYCON"]/table[1]/tr/td/a'
SEL_ALLOW_PLACES = '//div[@id="download_countries"]/text()'

SEL_LIST_MORE = '//div[@id="BODYCON"]/div[contains(text(),"More Accommodations")]/a'
place_sel_name = re.compile(r'Lodging in\s*(.*)<', re.DOTALL)
place_sel_link = re.compile(r'href="(.*)"', re.DOTALL)

SEL_LIST_PLACES_LAST = '//div[@id="BODYCON"]/table[1]/tr/td/div/a'
place_sel_name_last = re.compile(r'>(.*)<', re.DOTALL)
place_sel_link_last = re.compile(r'href="(.*)"', re.DOTALL)
place_sel_place_type = re.compile(r'<span class="placeTypeText">(.*)</span>', re.DOTALL)

# selectors for pages by language
SEL_JAPANESE_PAGE = '/html/head/link[@hreflang="ja"]/@href'
SEL_SPANISH_PAGE = '/html/head/link[@hreflang="es"]/@href'
SEL_FRENCH_PAGE = '/html/head/link[@hreflang="fr"]/@href'
SEL_CHINESE_PAGE = '/html/head/link[@hreflang="zh-Hans"]/@href'

# Selector for name of Place
SEL_HOTEL_NAME = '//h1[@id="HEADING" and (@rel="v:name" or @property="v:name")]/text()'

# Selector for address
SEL_AREA_NAME = '//div[@id="HEADING_GROUP"]/div/address/text()'
SEL_AREA_STREET = '//div[@id="HEADING_GROUP"]/div/address/span/span/span[@property="v:street-address"]/text()'
SEL_AREA_LOCALITY = '//div[@id="HEADING_GROUP"]/div/address/span/span/span/span[@property="v:locality"]/text()'
SEL_AREA_REGION = '//div[@id="HEADING_GROUP"]/div/address/span/span/span/span[@property="v:region"]/text()'
SEL_AREA_ZIP = '//div[@id="HEADING_GROUP"]/div/address/span/span/span/span[@property="v:postal-code"]/text()'


# Selector for amenities
SEL_AMENITIES = '//div[contains(@class, "amenitiesRDV1")]/div[contains(@class,"amenity")]/text()'

# Selector for phone number
SEL_PHONE_NUMBER = '//div[@id="HEADING_GROUP"]/div[contains(@class, "wrap")]'
SEL_RE_PHONE_NUMBER = re.compile(u'escramble.+?document', re.DOTALL)
# Selector for URL
SEL_URL = '//div[@id="HEADING_GROUP"]/div[contains(@class, "wrap")]'
SEL_RE_URL = re.escape(u'/ShowUrl?&excludeFromVS') + '.*?(?=")'

# Selector for rating
SEL_RATING = '//div[@id="HEADING_GROUP"]/div/address/span/span[contains(@class,"rate")]/img/@alt'
SEL_PERCENT = '//div[@class="recommendedPercent"]/span[@class="percent"]/text()'

# Selector for breadcrumbs
SEL_BREADCRUMBS = '//ul[@class="breadcrumbs"]/li/a/span/text()'

# Selector for body (just select few parts of the page !! dont' be so greedy!)
SEL_HEADING = '//div[@id="HEADING_GROUP"]'
SEL_META = '//head/meta'
SEL_AMENITY_DIV = '//div[@id="AMENITIES_OVERLAY_HIDDEN"]'
SEL_LOCATION_CONTENT = '//div[@id="HR_HACKATHON_CONTENT"]/div/div[contains(@class,"locationContent")]'

CLEAN_STATE = re.compile(r'(.*)\s\(', re.DOTALL)
FIND_HOTEL_LINK = re.compile(r'(?i)hotel', re.DOTALL)

BUS_SELECT_COORDINATE_ID = re.compile(r'idref="n\d+', re.DOTALL)


def get_body(sel):
  """extract the most relevant info from the page."""
  body = []
  body.append(sel.xpath(SEL_HEADING).extract())
  body.append(sel.xpath(SEL_META).extract())
  body.append(sel.xpath(SEL_AMENITY_DIV).extract())
  body.append(sel.xpath(SEL_LOCATION_CONTENT).extract())
  body = [b[0] for b in body if b and len(b)]
  return body


def clean_lf(value, sep=u''):
  if isinstance(value, dict):
    return value
  elif isinstance(value, (list, tuple)):
    return sep.join(value).replace('\n', '')
  else:
    return value.replace('\n', '')


def rev_telephone(scrambled):
  a2_or_1 = scrambled.split('var')
  a2_or_1 = u''.join([x for x in a2_or_1 if u'E' not in x])
  # print a2_or_1

  telephone = {}
  commands = a2_or_1.split('\n')
  # print commands
  for command in commands:
    # print command
    letter = command.split(u'=')
    if len(letter) >= 2:
      if u'+' in letter[0]:
        telephone['%s' % letter[0][0]] += letter[1].strip(u'\'')
      else:
        telephone['%s' % letter[0]] = letter[1].strip(u'\'')
  # print telephone
  try:
    phone_number = telephone['a'] + telephone['c'] + telephone['b']
  except:
    phone_number = u''
  return phone_number


def get_weburl(url):
  try:
    fp = urllib.urlopen(url)
  except:
    return u''
  return fp.geturl()


def debug_screen(value):
  """print any value on screen."""
  print ".*." * 50
  print value
  print ".*." * 50
