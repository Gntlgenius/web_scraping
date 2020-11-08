# -*- coding: utf-8 -*-
import scrapy
from zillow.utils import URL, cookie_parser, parse_url
from zillow.items import ZillowItem
from scrapy.loader import ItemLoader
import json


class PropertiesSpider(scrapy.Spider):
    name = 'properties'
    allowed_domains = ['www.zillows.com']

    page_num = iter(range(2,6))
   

    def start_requests(self):
        yield scrapy.Request(
            url = URL,
            callback = self.parse,
            cookies = cookie_parser(),
            meta={
                'currentPage':2
            }
           
        )

    def parse(self, response):
        resp = json.loads(response.body)
        current_page = response.meta['currentPage']
        properties = resp.get('searchResults').get('listResults')    
        for prop in properties:
            loader = ItemLoader(item=(ZillowItem()))
            loader.add_value('image_source', prop.get('imgSrc'))
            loader.add_value('status_Type', prop.get('statusType'))
            loader.add_value('price', prop.get('price'))
            loader.add_value('address', prop.get('address'))
            loader.add_value('Zipcode', prop.get('addressZipcode'))
            loader.add_value('house_details', prop.get('detailUrl'))
            loader.add_value('beds', prop.get('beds'))
            loader.add_value('baths', prop.get('baths'))
            loader.add_value('latitude', prop.get('latLong').get('latitude'))
            loader.add_value('longitude', prop.get('latLong').get('longitude'))
            yield loader.load_item()

        
        
        total_pages = 20
        if current_page <= total_pages:
            current_page+= 1
            yield scrapy.Request(
                url=parse_url(URL, pagenumber=current_page),
                callback=self.parse,
                cookies=cookie_parser(),
                meta={
                    'currentPage': current_page
                }
            )

    
