# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class Listing2Spider(scrapy.Spider):
    name = 'listing2'
    allowed_domains = ['www.centris.ca']


    position = {
            'startPosition':0
    }


    script= """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return splash:html()      
        end
    """
    def strip_character(self, val):
        return val.strip()


    def change_lang(self, value):
        new = value.replace("fr","en")
        return new

    def start_requests(self):
        yield scrapy.Request(
            url= "https://www.centris.ca/UserContext/Lock",
            method = "POST",
            headers={
                'x-requested-with': "XMLHttpRequest",
                'content-type':'application/json',
            },
            body = json.dumps({"uc":0}),
            callback= self.generate_uck
        )

    def generate_uck(self, response):
        uck = response.body
        query = {"query":{"UseGeographyShapes":0,"Filters":[{"MatchType":"CityDistrictAll","Text":"Montréal (All boroughs)","Id":5}],"FieldsValues":[{"fieldId":"CityDistrictAll","value":5,"fieldConditionId":"","valueConditionId":""},{"fieldId":"Category","value":"Residential","fieldConditionId":"","valueConditionId":""},{"fieldId":"SellingType","value":"Rent","fieldConditionId":"","valueConditionId":""},{"fieldId":"LandArea","value":"SquareFeet","fieldConditionId":"IsLandArea","valueConditionId":""},{"fieldId":"RentPrice","value":0,"fieldConditionId":"ForRent","valueConditionId":""},{"fieldId":"RentPrice","value":1000,"fieldConditionId":"ForRent","valueConditionId":""}]},"isHomePage":True}
        yield scrapy.Request(
            url = "https://www.centris.ca/property/UpdateQuery",
            method = "POST",
            body = json.dumps(query),
            headers = {
                'content-type':"application/json",
                'x-centris-uc': 0,
                'x-centris-uck':uck,
                'x-requested-with': "XMLHttpRequest"

            },
            callback = self.update_query
        )

    def update_query(self, response):
        yield scrapy.Request(
            url = "https://www.centris.ca/Property/GetInscriptions",
            method = "POST",
            body = json.dumps(self.position),
            headers = {
                'content-type':'application/json'
            },
            callback = self.parse
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')
        sel = Selector(text=html)
        for properties in sel.xpath("//div[@class='shell']"):
            val = properties.xpath(".//div[@class='price']/span[1]/text()").get()
            image_link = properties.xpath(".//div[1]/a/img/@src").get()
            address = properties.xpath(".//div[@class='location-container']/span[2]/div[1]/text()").get()
            city = properties.xpath(".//div[@class='location-container']/span[2]/div[2]/text()").get()
            zone = properties.xpath(".//div[@class='location-container']/span[2]/div[3]/text()").get()
            summ = properties.xpath("(.//following::a[@class='a-more-detail']/@href)[1]").get()
            summary = self.change_lang(summ)
            absolute_url = f"https://www.centris.ca{summary}"

            yield SplashRequest(
                url = absolute_url,
                endpoint = 'execute',
                callback = self.parse_summary,
                args ={
                    'lua_source':self.script
                },
                meta = {
                    'img':image_link
                    
                }
            )
        count = resp_dict.get('d').get('Result').get('count')
        increment = resp_dict.get('d').get('Result').get('inscNumberPerPage')
        if self.position['startPosition'] <= count:
            self.position['startPosition'] += increment
            yield scrapy.Request(
            url = "https://www.centris.ca/Property/GetInscriptions",
            method = "POST",
            body = json.dumps(self.position),
            headers = {
                'content-type':'application/json'
            },
            callback = self.parse
        )

    
    def parse_summary(self, response):
        add = response.xpath("(//h2[@itemprop='address']/text())[1]").get()
        price = response.xpath("(//div[@class='price']/span[4]/text())[1]").get()
        desc = response.xpath("normalize-space(//div[@itemprop='description']/text())").get()
        fea1 = response.xpath("normalize-space(//div[@class='col-lg-3 col-sm-6 piece']/text())").get()
        fea2 = response.xpath("normalize-space(//div[@class='col-lg-3 col-sm-6 cac']/text())").get()
        fea3 = response.xpath("normalize-space(//div[@class='col-lg-3 col-sm-6 sdb']/text())").get()
        #year_built = response.xpath("//div[@class='carac-value']/span/text()").get()
        agent = response.xpath("(//span[@itemprop='name']/text())[1]").get()
        contact = response.xpath("//div[@class='broker-contact-btn col-12 col-sm-4']/span/@href").get()
        img = response.request.meta['img']

        yield {
            'address':add,
            'price':price,
            'description':desc,
            'image_url':img,
            'feature1':fea1,
            'feature2':fea2,
            'feature3':fea3,
            #'year_built':year_built,
            'agent_name':agent,
            'agent_contact_link':contact
        }   
         

