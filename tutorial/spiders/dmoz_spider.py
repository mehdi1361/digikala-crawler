import scrapy
from tutorial.items import DmozItem
from tutorial.models import *

class MobileSpider(scrapy.Spider):
    name = "cwl_mob"
    # allowed_domains = ["dmoz.org"]

    def __init__(self, category=None, *args, **kwargs):
        super(MobileSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.digikala.com/Main/%s' % category]

    def parse(self, response):
        count = 1
        for sel in response.xpath('//ul/li/a[@class="brand"]'):
            item = DmozItem()
            # item = Category()
            # item.category_unique = 'mobile-%s' % sel.xpath('span[@class="left"]/text()').extract()
            # item.category_link = sel.xpath('@href').extract()
            # item.category_name = sel.xpath('span[@class="left"]/text()').extract()
            # yield item
            item['title']= 'mobile-%s' % sel.xpath('span[@class="left"]/text()').extract()
            item['link']= sel.xpath('@href').extract()
            item['category']= sel.xpath('span[@class="left"]/text()').extract()
            yield item
            try:
                category = Category.create(category_unique=str(count), category_name='mehdi', category_link='link')
                category.save()
            except:
                print 'error'
            # item.save()

class ProductSpider(scrapy.Spider):
    name = "cwl_pdt"

    def __init__(self, *args, **kwargs):
        super(MobileSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.digikala.com/Main/%s']
