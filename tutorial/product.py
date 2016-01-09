import requests
import re
import json
from pprint import pprint
from DataBase import *

categories = get_category_brand()
for category in categories:
    for page_number in range(1000):

        str_url = 'http://search.digikala.com/api/search/?category=%s&brand=%s&pageno=%s' % (category[0],
                                                                                             category[1],
                                                                                             page_number)
        pprint(str_url)
        req = requests.get(str_url)
        resp = json.loads(req.text)
        for item in resp['hits']['hits']:
            data = {
                'AnnounceDate': item['_source']['AnnounceDate'],
                'BrandId': item['_source']['BrandId'],
                'CategoryId': item['_source']['CategoryId'],
                'DetailSource': item['_source']['DetailSource'],
                'EStatus': item['_source']['EStatus'],
                'EnTitle': item['_source']['EnTitle'],
                'ExistStatus': item['_source']['ExistStatus'],
                'FaTitle': item['_source']['FaTitle'],
                'FavoriteCounter': item['_source']['FavoriteCounter'],
                'GiftSource': item['_source']['GiftSource'],
                'HasGift': item['_source']['HasGift'],
                'HasVideo': item['_source']['HasVideo'],
                'Id': item['_source']['Id'],
                'ImagePath': item['_source']['ImagePath'],
                'LastPeriodFavoriteCounter': item['_source']['LastPeriodFavoriteCounter'],
                'LastPeriodLikeCounter': item['_source']['LastPeriodLikeCounter'],
                'LastPeriodSaleCounter': item['_source']['LastPeriodSaleCounter'],
                'LastPeriodViewCounter': item['_source']['LastPeriodViewCounter'],
                'LikeCounter': item['_source']['LikeCounter'],
                'MaxPrice': item['_source']['MaxPrice'],
                'MinPrice': item['_source']['MinPrice'],
                'MinPriceList': item['_source']['MinPriceList'],
                'ProductTypes': item['_source']['ProductTypes'],
                'Rate': item['_source']['Rate'],
                'ReducedPrice': item['_source']['ReducedPrice'],
                'RegDateTime': item['_source']['RegDateTime'],
                'ShowType': item['_source']['ShowType'],
                'UrlCode': item['_source']['UrlCode'],
                'UserRating': item['_source']['UserRating'],
                'ViewCounter': item['_source']['ViewCounter'],
            }
            set_product.delay(**data)
            pprint(data)
            # pprint(item['_source'])
        # print page_number
        if not resp['hits']['hits']:
            break
