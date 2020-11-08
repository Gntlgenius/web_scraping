# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from games.items import GamesItem


class WithloaderSpider(scrapy.Spider):
    name = 'withloader'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?sort_by=&sort_order=0&filter=topsellers&page=1']

    def parse(self, response):
        All = response.xpath("//div[@id='search_resultsRows']/a")
        for games in All:
            loader = ItemLoader(item=GamesItem(), selector=games, response=response)
            loader.add_xpath('game_url', ".//@href")
            loader.add_xpath('game_img', ".//div[@class = 'col search_capsule']/img/@src")
            loader.add_xpath('game_name', ".//span[@class = 'title']/text()")
            loader.add_xpath('release_date', ".//div[@class='col search_released responsive_secondrow']/text()")
            loader.add_xpath('platforms', ".//span[contains(@class, 'platform_img') or @class='vr_supported']/@class")
            loader.add_xpath('original_price', ".//div[contains(@class, 'search_price_discount_combined')]")
            loader.add_xpath('review_summary', ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath('discounted_price', ".//div[contains(@class, ' search_price discounted')]/text()[2]")
            loader.add_xpath('discount_rate', ".//div[contains(@class, 'col search_discount responsive_secondrow')]/span/text()")
            yield loader.load_item()




        next_page = response.xpath("//a[contains(text(), '>') and @class = 'pagebtn']/@href").get()
        if next_page:
            yield scrapy.Request(
                url = next_page,
                callback = self.parse
            )


