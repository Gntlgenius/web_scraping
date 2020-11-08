# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class ZillowItem(scrapy.Item):
    image_source = scrapy.Field(
        output_processor = TakeFirst() 
    )
    status_Type = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    address = scrapy.Field(
        output_processor = TakeFirst()
    )
    Zipcode = scrapy.Field(

        output_processor = TakeFirst()
    )
    house_details = scrapy.Field(
        output_processor = TakeFirst()
    )
    beds = scrapy.Field(
        output_processor = TakeFirst()
    )
    baths = scrapy.Field(
        output_processor = TakeFirst()
    )
    latitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    longitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    







   