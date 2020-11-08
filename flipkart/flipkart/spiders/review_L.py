# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from flipkart.items import FlipkartItem


class ReviewsSpider(scrapy.Spider):
    name = 'reviews_L'
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
                item = response.xpath("//div[@class='o9Xx3p _1_odLJ']/text()").get()
                for reviewz in response.xpath("//div[@class='_1PBCrt']"):
                    ratingz = reviewz.xpath(".//div[@class='hGSR34 E_uFuv']/text()").get()
                    captionz = reviewz.xpath(".//p[@class='_2xg6Ul']/text()").get()
                    commentz = reviewz.xpath(".//div[@class='qwjRop']/div/div/text()").getall()
                    review_time= reviewz.xpath(".//p[@class='_3LYOAd']/text()").get()
                    loader = ItemLoader(item=FlipkartItem())
                    loader.add_value('item_desc', item)
                    loader.add_value('ratings', ratingz)
                    loader.add_value('caption', captionz)
                    loader.add_value('comments', commentz)
                    loader.add_value('time_reviewed', review_time)
                    yield loader.load_item()
                   
                    
                
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



        

