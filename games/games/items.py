# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.selector import Selector



def platform_list(one_class): 
    plat = []   
    found = one_class.split(" ")[-1]
    plat.append(found)
    
    return plat

def get_origPrice(html_markup):
    originalPrice = ''

    selector_obj = Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(".//div[contains(@class, 'search_price discounted')]")
    if len(div_with_discount) > 0:
        originalPrice = div_with_discount.xpath(".//span/strike/text()").get()
    else:
        originalPrice = selector_obj.xpath(".//div[contains(@class, 'search_price')]/text()").getall()
    return originalPrice

def clean_review(review):
    if review:
        return review.replace('<br>', ' ')
    else:
        return "No Reviews"


def clean_discount_price(price):
    if price:
        return price.strip()
    else:
        return "$0"



def clean_discount(val):
    if val :
        return  val.strip('-')
    else:
        return "No Discount"

class GamesItem(scrapy.Item):
    game_url  = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_img  = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name  = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date  = scrapy.Field(
        output_processor=TakeFirst()
    )
    platforms  = scrapy.Field(
        input_processor=MapCompose(platform_list)
    )
    original_price  = scrapy.Field(
        input_processor= MapCompose(get_origPrice, str.strip),
        output_processor=Join('')
    )
    review_summary  = scrapy.Field(
        input_processor = MapCompose(clean_review),
        output_processor = TakeFirst()
    )
    discounted_price  = scrapy.Field(
        input_processor = MapCompose(clean_discount_price),
        output_processor = TakeFirst()
    )
    discount_rate  = scrapy.Field(
        input_processor = MapCompose(clean_discount),
        output_processor = TakeFirst()
    )
    
    