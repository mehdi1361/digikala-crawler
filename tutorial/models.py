import peewee
from peewee import *


mysql_db = peewee.MySQLDatabase('my_database', user='root', passwd='13610522',host='127.0.0.1')



class Category(Model):
    category_unique = CharField(primary_key=True)
    category_name = CharField()
    category_link = CharField(max_length=1000)

    class Meta:
        databases = mysql_db

mysql_db.connect()

# mysql_db.create_table(Category)
