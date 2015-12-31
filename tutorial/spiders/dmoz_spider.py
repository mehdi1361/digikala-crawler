import scrapy
from tutorial.items import DmozItem
from tutorial.DataBase import *


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


class ProductSpider(scrapy.Spider):
    name = "cwl_pdt"

    def __init__(self, category=None, url=None, category_type=None, *args, **kwargs):
        self.category = category
        self.category_type = category_type
        self.start_urls = ['http://www.digikala.com%s/PageNo-1/' % url]
        super(ProductSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        pass
        print self.category
        print self.start_urls
        count = 0
        print count

        for sel in response.xpath('//div[@id="products"]'):
            print 'aaa', sel.xpath('div/text()').extract()

        # for sel in response.xpath('//div[@id="products"]'):
        #     print 'ok'
        #     print sel.xpath('div/a/@href').extract()
        #     item = DmozItem()
        #     item['title'] = 'mobile'
        #     item['link'] = sel.xpath('@href').extract()
        #     item['category'] = 'test'
        #     count += 1
        #     print count
        #     yield item

