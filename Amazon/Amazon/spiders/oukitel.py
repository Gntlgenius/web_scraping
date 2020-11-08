# -*- coding: utf-8 -*-
import scrapy
import json
from Amazon.utils import cookie_parser


class OukitelSpider(scrapy.Spider):
    name = 'oukitel'
    allowed_domains = ['www.amazon.com']
    start_urls = ["https://www.amazon.co.uk/s?k=oukitel&qid=1603434367&ref=sr_pg_1"]


    
        

    def parse(self, response):
        items = response.xpath("//div[@class='a-section a-spacing-medium']")
        for item in items:
            yield {
                'phone_name':item.xpath(".//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/a/span/text()").get(),
                'currency':item.xpath(".//span[@class='a-price-symbol']/text()").get(),
                'phone_price':item.xpath(".//span[@class='a-price-whole']/text()").get(),
                'phone_link':item.xpath(".//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/a/@href").get()
            }

        next_page = response.xpath("//ul[@class='a-pagination']/li[7]/a/@href").get()
        if next_page:
            yield scrapy.Request(
                url = response.urljoin(next_page),
                callback=self.parse
            )