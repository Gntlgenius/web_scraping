# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from w3lib.html import remove_tags
from scrapy.selector import Selector


class RecordsSpider(scrapy.Spider):
    name = 'records'
    allowed_domains = ['www.bog.gov.gh']


    script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(2))
            return splash:html()
   
        end
    """

    def start_requests(self):
        yield SplashRequest(url="https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates", callback=self.parse, endpoint="execute", args={
                    'lua_source':self.script
        })


            
    def parse(self, response):
        for data in response.xpath("//table[@id='table_1']/tbody/tr"):
            yield {
                'date':data.xpath(".//td[1]/text()").get(),
                'currency':data.xpath(".//td[2]/text()").get(),
                'currency_pair':data.xpath(".//td[3]/text()").get(),
                'buying':data.xpath(".//td[4]/text()").get(),
                'selling':data.xpath(".//td[5]/text()").get(),
                'mid_rate':data.xpath(".//td[6]/text()").get(),
            }
        

        next_page = 
        
