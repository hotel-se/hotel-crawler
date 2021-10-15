import scrapy

import json
from src.items import Hotel

class TripadvisorSpider(scrapy.Spider):
  name = 'tripadvisor'
  start_urls = [
    'https://www.tripadvisor.com/Hotels-g187768-Italy-Hotels.html',
    'https://www.tripadvisor.com/Hotels-g188045-Switzerland-Hotels.html'
  ]


  def parse(self, response):
    els = 0

    for hotel in response.css('.listItem'):
      els += 1

      hotel_obj = Hotel()

      hotel_obj['url'] = f'https://tripadvisor.com/{str(hotel.css(".meta_listing::attr(data-url)").extract()[0]).strip()}'
      hotel_obj['name'] = str(hotel.css('.listing_title>a::text').extract()[0]).strip()

      yield scrapy.Request(response.urljoin(hotel_obj['url']),
                           callback=self.parse_details,
                           cb_kwargs=dict(hotel=hotel_obj))

      if els % 30 == 0:
        request = {
          'offset': f'{els}'
        }

        headers = {
          'x-puid': '96449683-5e31-4b47-9440-e197195db75e',
          'DNT': '1',
          'authority': 'www.tripadvisor.com',
          'accept': 'text/html, */*',
          'x-requested-with': 'XMLHttpRequest',
          'referer': f'{response.request.url}'
        }

        yield scrapy.FormRequest(response.request.url,
                                 method= "POST",
                                 callback=self.parse,
                                 formdata=request,
                                 headers=headers)


  def parse_details(self, response, hotel):
    hotel['address'] = str(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "yYjkv", " " ))]/text()').extract()[0]).strip()
    hotel['price'] = None
    
    rating = response.css('.bvcwU::text').extract()[0]
    n_ratings = response.css('.btQSs::text').extract()[0].split(' ')[0]
    hotel['rating'] = {'score': rating, 'n_ratings': n_ratings}

    try:
      description = json.loads(response.css('#ABOUT_TAB>div.ui_columns.uXLfx>div:nth-child(1)>div:nth-child(7)::attr(data-ssrev-handlers)').extract()[0])
      hotel['description'] = description['load'][3]['locationDescription']
    except (IndexError, KeyError):
      description = json.loads(response.css('#ABOUT_TAB>div.ui_columns.uXLfx>div:nth-child(1)>div:nth-child(8)::attr(data-ssrev-handlers)').extract()[0])
      hotel['description'] = description['load'][3]['locationDescription']
    
    try:
      hotel['phone_number'] = str(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mEnKG", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "ceIOZ", " " ))]/text()').extract()[0]).strip()
    except IndexError:
      hotel['phone_number'] = None

    yield hotel
