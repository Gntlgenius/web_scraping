# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from w3lib.html import remove_tags
from scrapy.selector import Selector


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['www.flipkart.com']

    script = '''
       function main(splash, args)
            splash.private_mode_enabled=false
            assert(splash:go(args.url))
            assert(splash:wait(2))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    num = iter(range(2,10))

    try:
            item_name = "iphone 11"
            def start_requests(self):
                yield SplashRequest(url=f"https://www.flipkart.com/search?q={self.item_name}", callback=self.parse, endpoint="execute", args={
                    'lua_source':self.script
                })


            def parse(self, response):
                #print(response.body)
                item = response.xpath("//a[@class='_31qSD5']/@href")[0].get()
                item_url = response.urljoin(item)
                #print(f'THE ITEM URL ={item_url}')


                yield SplashRequest(
                    url = item_url,
                    endpoint = 'execute',
                    callback = self.parse_summary,
                    args ={
                        'lua_source':self.script
                    }
                )

                

            def parse_summary(self, response):
                reviews = response.xpath("//div[@class='col _39LH-M']/a/@href").get()
                reviews_url = response.urljoin(reviews)

                yield SplashRequest(
                    url = reviews_url,
                    endpoint = 'execute',
                    callback = self.parse_comments,
                    args ={
                        'lua_source':self.script
                    }
                )


            def parse_comments(self, response):
                for reviewz in response.xpath("//div[@class='_1PBCrt']"):
                    yield {
                        'rating':reviewz.xpath(".//div[@class='hGSR34 E_uFuv']/text()").get(),
                        'caption':reviewz.xpath(".//p[@class='_2xg6Ul']/text()").get(),
                        'comments':reviewz.xpath(".//div[@class='qwjRop']/div/div/text()").getall()
                    }
                
                next = response.xpath("//a[@class='_3fVaIS']/@href").getall()
                next_page = response.urljoin(next[-1])
                if next:
                     yield SplashRequest(
                        url = next_page,
                        endpoint = 'execute',
                        callback = self.parse_comments,
                        args ={
                            'lua_source':self.script
                        }
                    )


                
                
    except Exception as e:
        print(e)



        

