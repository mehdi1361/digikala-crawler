import MySQLdb
import datetime
import memcache
import json
import requests

from celery import Celery

app = Celery('digikala', broker='amqp://guest@localhost//')


class Caching(object):
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server = memcache.Client([self.hostname])

    def set(self, key, value, expiry=900):
        self.server.set(key, value, expiry)

    def get(self, key):
        return self.server.get(key)

    def delete(self, key):
        self.server.delete(key)


@app.task
def insert_category(category_unique, category_name, category_link):

    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = '''INSERT INTO category(category_unique,category_name,category_link) VALUES('%s', '%s', '%s');''' % (
        '%s-%s' % (str(category_unique), str(category_name[0])), str(category_name[0]), str(category_link[0]))
    result = cursor.execute(sql_string)
    # WriteToFile.delay(category_unique, result)
    db.commit()
    db.close()

def get_category():
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = '''select category_link from my_database.category;'''
    print sql_string
    cursor.execute(sql_string)
    result = cursor.fetchall()
    links =[]
    for row in result:
        links.append(row[0])
    # WriteToFile.delay(category_unique, result)
    db.commit()
    db.close()
    return links

def get_category_brand():
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = '''select categorycode,BrandCode from my_database.category;'''
    cursor.execute(sql_string)
    result = cursor.fetchall()
    links =[]
    for row in result:
        links.append(row)
    # WriteToFile.delay(category_unique, result)
    db.commit()
    db.close()
    return links

def get_products_id():
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = '''select id from products;'''
    print sql_string
    cursor.execute(sql_string)
    result = cursor.fetchall()
    products =[]
    for row in result:
        products.append(row[0])
    # WriteToFile.delay(category_unique, result)
    db.commit()
    db.close()
    return products

@app.task
def set_product(AnnounceDate, BrandId, CategoryId, DetailSource, EStatus, EnTitle,
                      ExistStatus, FaTitle, FavoriteCounter, GiftSource,
                     HasGift, HasVideo, Id, ImagePath, LastPeriodFavoriteCounter,
                     LastPeriodLikeCounter, LastPeriodSaleCounter, LastPeriodViewCounter, LikeCounter, MaxPrice,
                     MinPrice, MinPriceList, ProductTypes, Rate, ReducedPrice, RegDateTime, ShowType, UrlCode,
                     UserRating, ViewCounter):
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = ''' insert into products(AnnounceDate, BrandId, CategoryId, DetailSource, EStatus, EnTitle,
                      ExistStatus, FaTitle, FavoriteCounter, GiftSource,
                     HasGift, HasVideo, Id, ImagePath, LastPeriodFavoriteCounter,
                     LastPeriodLikeCounter, LastPeriodSaleCounter, LastPeriodViewCounter, LikeCounter, MaxPrice,
                     MinPrice, MinPriceList, ProductTypes, Rate, ReducedPrice, RegDateTime, ShowType, UrlCode,
                     UserRating, ViewCounter) VALUES('%s', %s, %s,'%s',%s,'%s',%s,'%s',%s,'%s','%s','%s',%s,'%s',%s,
                     %s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,'%s',%s,'%s',%s,%s)''' % (AnnounceDate, BrandId, CategoryId, DetailSource, EStatus, EnTitle,
                      ExistStatus, FaTitle, FavoriteCounter, GiftSource,
                     HasGift, HasVideo, Id, ImagePath, LastPeriodFavoriteCounter,
                     LastPeriodLikeCounter, LastPeriodSaleCounter, LastPeriodViewCounter, LikeCounter, MaxPrice,
                     MinPrice, MinPriceList, ProductTypes, Rate, ReducedPrice, RegDateTime, ShowType, UrlCode,
                     UserRating, ViewCounter)
    result = cursor.execute(sql_string)
    download_product_image(Id, ImagePath)
    db.commit()
    db.close()

@app.task
def set_product_detail(id_product, specs_title, specs_value, wiki):
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    cursor.execute('set names utf8;')
    sql_string = '''INSERT INTO product_detail
                    (id_product,specs_title,specs_value,wiki)
                    VALUES(%s , '%s' , '%s', '%s');''' % (id_product, specs_title.encode('utf-8'), specs_value.encode('utf-8'), wiki.encode('utf-8'))
    print sql_string
    result = cursor.execute(sql_string)
    db.commit()
    db.close()

@app.task
def download_product_image(product_id, product_image_url):
    url = "http://file.digikala.com/Digikala/%s" % product_image_url
    response = requests.get(url)
    local_image_url = "product_image/%s.jpg" % product_id
    if response.status_code == 200:
        f = open(local_image_url, 'wb')
        f.write(response.content)
        f.close()
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "my_database")
    cursor = db.cursor()
    sql_string = '''INSERT INTO product_images(product_id,product_images_url)VALUES(%s,'%s');''' % (product_id, local_image_url)
    result = cursor.execute(sql_string)
    db.commit()
    db.close()
@app.task
def WriteToFile(TransactionId, Result):
    print "Hello"
    f = open('Log/myfile.out', 'a')
    f.write('update DataBase with transactionId: %s Successfull:{%s} at :%s\n' % (
        TransactionId, Result, datetime.datetime.now()))
    f.close()
