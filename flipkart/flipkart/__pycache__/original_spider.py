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
                print(f'THE ITEM URL ={item_url}')


                    yield SplashRequest(
                            url = item_url,
                            endpoint = 'execute',
                            callback = self.parse_summary,
                            args ={
                                'lua_source':self.script
                            }
                    )

                
            #     next_page = f'https://www.flipkart.com/search?q=LAPTOPS&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={next(self.num)}'
                
                
            #     yield SplashRequest(
            #         url=next_page, 
            #         callback=self.parse, 
            #         endpoint="execute", 
            #         args={'lua_source':self.script
            #         }
            #     )

            # def parse_summary(self, response):
            #     nxt_url = response.xpath("//a[@class='_2Xp0TH']/@href").get()
            #     image_src = response.xpath("//div[@class='_1ov7-N']/div[2]/img/@src").get()
            #     laptop_name = response.xpath("//h1[@class='_9E25nV']/span/text()[1]").get()
            #     Avg_rating = response.xpath("//div[@class='_3ors59']/div/span[1]/div/text()").get()
            #     review_caption = response.xpath("//p[@class='_2xg6Ul']/text()").get()
            #     reviews = response.xpath("(//div[@class='qwjRop']/div/div/text())[1]").get()
            #     #//a[@class ='_3fVaIS']/@href
            #     #next_page = response.xpath("//a[@class='_3fVaIS']/span/text()").get()
            #     yield {

            #         'nxt_url':nxt_url,
            #         'image_src':image_src,
            #         'laptop_name':laptop_name,
            #         'Avg_rating':Avg_rating,
            #         'review_caption':review_caption,
            #         'reviews':reviews           

            #    }
    except Exception as e:
        print(e)



        

