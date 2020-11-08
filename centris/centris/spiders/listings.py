# -*- coding: utf-8 -*-
import scrapy
import json


class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['www.centris.ca/en']


    position = {
            'startPosition':0
    }

    

    def start_requests(self):
           
        query = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                {
                    "MatchType": "CityDistrictAll",
                    "Text": "Montréal (All boroughs)",
                    "Id": 5
                }
                ],
                "FieldsValues": [
                {
                    "fieldId": "CityDistrictAll",
                    "value": 5,
                    "fieldConditionId": "",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "Category",
                    "value": "Residential",
                    "fieldConditionId": "",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "SellingType",
                    "value": "Rent",
                    "fieldConditionId": "",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "LandArea",
                    "value": "SquareFeet",
                    "fieldConditionId": "IsLandArea",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "RentPrice",
                    "value": 0,
                    "fieldConditionId": "ForRent",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "RentPrice",
                    "value": 1000,
                    "fieldConditionId": "ForRent",
                    "valueConditionId": ""
                }
                ]
            },
            "isHomePage": True
        }
        yield scrapy.Request(
            url = "https://www.centris.ca/property/UpdateQuery",
            method = "POST",
            body = json.dumps(query),
            headers = {
                'content-type':"application/json",
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
        print(response.body)
        
