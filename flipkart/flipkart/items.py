# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class FlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    ratings = scrapy.Field(
        output_processor = TakeFirst() 
    )
    caption = scrapy.Field(
        output_processor = TakeFirst() 
    )
    comments = scrapy.Field(
        output_processor = TakeFirst() 
    )
    time_reviewed = scrapy.Field(
        output_processor = TakeFirst()
    )
    item_desc = scrapy.Field(
        output_processor = TakeFirst()
    )
    
