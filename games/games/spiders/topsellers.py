# -*- coding: utf-8 -*-
import scrapy


class TopsellersSpider(scrapy.Spider):
    name = 'topsellers'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?sort_by=&sort_order=0&filter=topsellers&page=1']

    def get_origPrice(self, selector_obj):
        originalPrice = ''
        div_with_discount = selector_obj.xpath(".//div[contains(@class, 'search_price discounted')]")
        if len(div_with_discount) > 0:
            originalPrice = div_with_discount.xpath(".//span/strike/text()").get()
        else:
            originalPrice = selector_obj.xpath(".//div[contains(@class, 'search_price')]/text()").get()
        return originalPrice.strip()

    def clean_discount(self, val):
        if val :
            return  val.strip('-')
        else:
            return "No Discount"

    def clean_review(self, review):
        if review:
            return review.replace('<br>', ' ')
        else:
            return "No Reviews"

    def platform_list(self, platforms):
        n= len(platforms)
        i=0
        plat = []
        while i < n:     
            found = platforms[i].split(" ")[-1]
            plat.append(found)
            i = i + 1
        return plat

    def clean_discount_price(self, price):
        if price:
            return price.strip()
        else:
            return "None"

            
        


    def parse(self, response):
        All = response.xpath("//div[@id='search_resultsRows']/a")
        for games in All:
            game_url = games.xpath(".//@href").get()
            game_img = games.xpath(".//div[@class = 'col search_capsule']/img/@src").get()
            platforms = self.platform_list(games.xpath(".//span[contains(@class, 'platform_img') or @class='vr_supported']/@class").getall())
            game_name = games.xpath(".//span[@class = 'title']/text()").get()
            release_date = games.xpath(".//div[@class='col search_released responsive_secondrow']/text()").get()
            original_price = self.get_origPrice(games.xpath(".//div[contains(@class, 'search_price_discount_combined')]"))
            discounted_price = self.clean_discount_price(games.xpath(".//div[contains(@class, ' search_price discounted')]/text()[2]").get())
            discount_rate = self.clean_discount(games.xpath(".//div[contains(@class, 'col search_discount responsive_secondrow')]/span/text()").get())
            review_summary = self.clean_review(games.xpath(".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html").get())
            yield {
                'game_url':game_url,
                'game_img':game_img,
                'game_name':game_name,
                'platforms':platforms,
                'release_date':release_date,
                'discounted_price':discounted_price,
                'original_price':original_price,
                'discount_rate':discount_rate,
                'review_summary':review_summary
                
            }

        next_page = response.xpath("//a[contains(text(), '>') and @class = 'pagebtn']/@href").get()
        if next_page:
            yield scrapy.Request(
                url = next_page,
                callback = self.parse
            )

