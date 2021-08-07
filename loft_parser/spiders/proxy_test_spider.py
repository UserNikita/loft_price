import scrapy
import json


class ProxySpider(scrapy.Spider):
    name = "proxy_test"

    start_urls = ["https://ipwhois.app/json/"]

    # def start_requests(self):
    #     yield scrapy.Request(
    #         self.start_urls[0],
    #         meta={'proxy': 'https://185.38.111.1:8080'},
    #         callback=self.parse
    #     )

    def parse(self, response):
        print('REQUEST\n', response.request.headers)
        print('RESPONSE\n', json.loads(response.body)['country'])
