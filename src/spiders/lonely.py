import scrapy

from src.items import Hotel
from src.coordinates import getCoordinates

class BookingSpider(scrapy.Spider):
  name = 'lonely'
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' 
  start_urls = [
    'https://www.lonelyplanet.com/italy/hotels?page=1&subtypes=Hotel',
    'https://www.lonelyplanet.com/switzerland/hotels?page=1&subtypes=Hotel'
  ]

  def parse(self, response):
    for i in range(1, 100):
      for hotel in response.css('.jsx-2276123283.flex.flex-col.items-center'):
        hotel_obj = Hotel()

        hotel_obj['name'] = str(hotel.css('.text-xl.text-primary.font-semibold.leading-tight::text').extract()[0])
        hotel_obj['url'] = 'https://www.lonelyplanet.com' + str(hotel.css('.jsx-2276123283.flex.flex-col.items-center::attr(href)').extract()[0])

        yield scrapy.Request(response.urljoin(hotel_obj['url']),
                             callback=self.parse_details,
                             cb_kwargs=dict(hotel=hotel_obj))

        page = i + 1
        next_page = response.request.url.split('page=')[0] + 'page=' + str(page) + '&subtypes=Hotel'

        yield scrapy.Request(next_page, callback=self.parse)


  def parse_details(self, response, hotel):
    try:
      hotel['address'] = str(response.css('.flex:nth-child(1)::text').extract()[0])
    except (IndexError, KeyError):
      hotel['address'] = None

    try:
      description = response.css('.body p::text').extract()
      final_description = ''

      for line in description:
        print(line)
        if line[-1] == ' ':
          final_description += line
        else:
          final_description += line + '\n'
      
      final_description = final_description[:-2]
    except (IndexError, KeyError):
      final_description = None

    getCoordinates(hotel)

    try:
      hotel['phone_number'] = str(response.css('a.jsx-1718619389::text').extract()[0])
    except (IndexError, KeyError):
      hotel['phone_number'] = None

    hotel['description'] = final_description
    hotel['rating'] = None
    hotel['source'] = 'lonely'
    
    yield hotel
