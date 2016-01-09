import scrapy
import json
from tutorial.items import DmozItem,DetailItem
from tutorial.DataBase import *
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule

class MobileSpider(scrapy.Spider):
    name = "cwl_mob"
    # allowed_domains = ["dmoz.org"]

    def __init__(self, category=None, *args, **kwargs):
        super(MobileSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.digikala.com/Main/%s' % category]

    def parse(self, response):
        for sel in response.xpath('//ul/li/a[@class="brand"]'):
            item = DmozItem()
            item['title'] = 'mobile'
            item['link'] = sel.xpath('@href').extract()
            item['category'] = sel.xpath('span[@class="left"]/text()').extract()
            self._data = {
                'category_unique': item['title'],
                'category_name': item['category'],
                'category_link': item['link']
            }
            insert_category(**self._data)
            yield item

class MobileSpider1(scrapy.Spider):
    name = "cwl_mob1"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://api.digikala.com/JzNMJGUkc7s=/wxzPbOeaJM2f7qjgetwqKg3HONlZKYBT?aqPI=43024&aqIIO=false&aqIP=false",
    ]

    def make_requests_from_url(self, url):
        request = super(MobileSpider1, self).make_requests_from_url(url)
        request.cookies['foo'] = 'bar'
        return request

    def parse(self, response):
        for sel in response.xpath('//ul/li/a[@class="brand"]'):
            item = DmozItem()
            item['title'] = 'mobile'
            item['link'] = sel.xpath('@href').extract()
            item['category'] = sel.xpath('span[@class="left"]/text()').extract()
            self._data = {
                'category_unique': item['title'],
                'category_name': item['category'],
                'category_link': item['link']
            }
            insert_category(**self._data)
            yield item

