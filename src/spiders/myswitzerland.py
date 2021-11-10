import scrapy

from src.items import Hotel
from src.coordinates import getCoordinates

class BookingSpider(scrapy.Spider):
  name = 'myswitzerland'
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' 
  start_urls = [
    'https://www.myswitzerland.com/en-ch/accommodations/hotel-search/'
  ]

  def parse(self, response):
    for hotel in response.css('.FilterGridView--item'):
      hotel_obj = Hotel()

      hotel_obj['name'] = hotel.css('.OfferTeaser--title span:not(.OfferTeaser--category)::text').extract()[0].strip()
      hotel_obj['url'] = hotel.css('.OfferTeaser--link::attr(href)').extract()[0].strip()

      yield scrapy.Request(response.urljoin(hotel_obj['url']),
                           callback=self.parse_details,
                           cb_kwargs=dict(hotel=hotel_obj))

    if response.css('.Pagination--link.next::attr(href)').extract()[0] is not None:
      yield response.follow(response.css('.Pagination--link.next::attr(href)').extract()[0], callback=self.parse)


  def parse_details(self, response, hotel):
    if response.css('.ArticleSubSection--content>.richtext::text').extract()[0].strip() != '':
      hotel['description'] = response.css('.ArticleSubSection--content>.richtext::text').extract()[0].strip()
    else:
      hotel['description'] = None

    address = ''

    for i in response.css('.CardTeaser--text p:not(.t-dark)::text').extract():
      address += i.strip()
      address += ' '

    try:
      hotel['address'] = address.strip().replace('\xa0', ' ')
    except (IndexError, KeyError):
      hotel['address'] = None

    getCoordinates(hotel)

    try:
      hotel['phone_number'] = response.css('.CardTeaser--text>p>.Link:not(.icon-after)::text').extract()[0].strip()
    except (IndexError, KeyError):
      hotel['phone_number'] = None

    hotel['rating'] = None
    hotel['source'] = 'myswitzerland'

    yield hotel
