import requests
import scrapy

from src.items import Hotel
from src.coordinates import getCoordinates

class BookingSpider(scrapy.Spider):
  name = 'booking'
  start_urls = [
    'https://www.booking.com/searchresults.html?label=gog235jc-1DCAEoggI46AdIM1gDaCyIAQGYATG4ARnIAQzYAQPoAQH4AQKIAgGoAgO4At-aoYsGwAIB0gIkMDRkNjUzODYtOTAyZC00ZmMwLWI0NzItNjUwMmI0Zjg0M2E22AIE4AIB&sid=1326848c94579486a72f91a211f60644&aid=397594&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=104&dest_type=country&from_sf=1&group_adults=2&group_children=0&label_click=undef&nflt=ht_id%3D204%3B&no_rooms=1&percent_htype_hotel=1&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&src=searchresults&srpvid=e26e6f1fcac00031&ss=Italy&ss_raw=Italy&ssb=empty&ssne=Trimouns+Talc+Quarry&ssne_untouched=Trimouns+Talc+Quarry&top_ufis=1&sig=v1E89SRDqL',
    'https://www.booking.com/searchresults.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaCyIAQGYATG4ARnIAQzYAQHoAQH4AQKIAgGoAgO4At-aoYsGwAIB0gIkMDRkNjUzODYtOTAyZC00ZmMwLWI0NzItNjUwMmI0Zjg0M2E22AIF4AIB&sid=1326848c94579486a72f91a211f60644&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=204&dest_type=country&from_sf=1&group_adults=2&group_children=0&label_click=undef&nflt=ht_id=204;&no_rooms=1&raw_dest_type=country&room1=A,A&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&src=searchresults&srpvid=013a6f44487d001f&ss=Switzerland&ss_raw=Swi&ssb=empty&top_ufis=1&sig=v1WoeMHM2-'
  ]

  # &offset=25

  def parse(self, response):
    for i in range(0, 100):
      for hotel in response.css('.hotellist_wrap'):
        hotel_obj = Hotel()

        yield scrapy.Request(f'{response.request.url}&offset={i*25}')

