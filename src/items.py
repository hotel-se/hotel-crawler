# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Hotel(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    coordinates = scrapy.Field()
    source = scrapy.Field()
