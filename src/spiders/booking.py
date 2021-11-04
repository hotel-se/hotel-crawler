import scrapy

from src.items import Hotel
from src.coordinates import getCoordinates

class BookingSpider(scrapy.Spider):
  name = 'booking'
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' 
  start_urls = [
    'https://www.booking.com/searchresults.html?label=gog235jc-1DCAEoggI46AdIM1gDaCyIAQGYATG4ARnIAQzYAQPoAQH4AQKIAgGoAgO4At-aoYsGwAIB0gIkMDRkNjUzODYtOTAyZC00ZmMwLWI0NzItNjUwMmI0Zjg0M2E22AIE4AIB&sid=1326848c94579486a72f91a211f60644&aid=397594&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=104&dest_type=country&from_sf=1&group_adults=2&group_children=0&label_click=undef&nflt=ht_id%3D204%3B&no_rooms=1&percent_htype_hotel=1&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&src=searchresults&srpvid=e26e6f1fcac00031&ss=Italy&ss_raw=Italy&ssb=empty&ssne=Trimouns+Talc+Quarry&ssne_untouched=Trimouns+Talc+Quarry&top_ufis=1&sig=v1E89SRDqL',
    'https://www.booking.com/searchresults.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaCyIAQGYATG4ARnIAQzYAQHoAQH4AQKIAgGoAgO4At-aoYsGwAIB0gIkMDRkNjUzODYtOTAyZC00ZmMwLWI0NzItNjUwMmI0Zjg0M2E22AIF4AIB&sid=1326848c94579486a72f91a211f60644&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=204&dest_type=country&from_sf=1&group_adults=2&group_children=0&label_click=undef&nflt=ht_id=204;&no_rooms=1&raw_dest_type=country&room1=A,A&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&src=searchresults&srpvid=013a6f44487d001f&ss=Switzerland&ss_raw=Swi&ssb=empty&top_ufis=1&sig=v1WoeMHM2-'
  ]

  def parse(self, response):
    for i in range(0, 1):
      for hotel in response.css('._fe1927d9e._0811a1b54._a8a1be610._022ee35ec.b9c27d6646.fb3c4512b4.fc21746a73'):
        hotel_obj = Hotel()

        hotel_obj['name'] = str(hotel.css('.fde444d7ef::text').extract()[0])
        hotel_obj['url'] = str(hotel.css('.fb01724e5b::attr(href)').extract()[0])

        rating = str(hotel.css('._9c5f726ff.bd528f9ea6::text').extract()[0])
        rating = str(float(rating) * 5 / 10)

        n_ratings = str(hotel.css('._4abc4c3d5._1e6021d2f._fb3ba087b._6e869d6e0::text').extract()[0].split(' ')[0])

        hotel_obj['rating'] = {'score': rating, 'n_ratings': n_ratings}

        yield scrapy.Request(response.urljoin(hotel_obj['url']),
                            callback=self.parse_details,
                            cb_kwargs=dict(hotel=hotel_obj))

      yield scrapy.Request(f'{response.request.url}&offset={i*25}')

  def parse_details(self, response, hotel):
    try:
      hotel['address'] = str(response.css('.hp_address_subtitle::text').extract()[0].strip())
    except (IndexError, KeyError):
      hotel['address'] = None

    hotel['phone_number'] = None
    hotel['price'] = None

    getCoordinates(hotel)

    description = '\n'.join(response.css('#property_description_content').extract()[0].split('<p>')[2:])
    description = description.replace('</p>\n', '')
    description = description.replace('</p>\n</div>', '')
    description = description.replace('<p>', '')
    description = description.replace('</div>', '')
    description = description.replace('<br>', '')

    hotel['description'] = description
    hotel['source'] = 'booking.com'

    yield hotel
