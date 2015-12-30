import MySQLdb
import datetime
import memcache
import json

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

@app.task
def WriteToFile(TransactionId, Result):
    print "Hello"
    f = open('Log/myfile.out', 'a')
    f.write('update DataBase with transactionId: %s Successfull:{%s} at :%s\n' % (
        TransactionId, Result, datetime.datetime.now()))
    f.close()
