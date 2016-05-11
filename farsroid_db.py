
import peewee as pw
db = pw.MySQLDatabase("farsroid_db", host="127.0.0.1", port=3306, user="root", passwd="13610522")

class Genre(pw.Model):
    genre_name = pw.CharField()
    genre_url = pw.CharField()
    class Meta:
        database = db

class Games_Urls(pw.Model):
    title = pw.CharField()
    url = pw.CharField()
    genre = pw.ForeignKeyField(Genre)

    class Meta:
        database = db

class Game_Description(pw.Model):
    title = pw.CharField()
    avatar = pw.CharField()
    detail = pw.TextField()
    apk = pw.CharField()
    trailer = pw.CharField()
    game = pw.ForeignKeyField(Games_Urls)

    class Meta:
        database = db

class Game_picture(pw.Model):
    url = pw.CharField()
    game_desc = pw.ForeignKeyField(Game_Description)
    file_name = pw.CharField()
    class Meta:
        database = db

# class Game_image(pw.Model):
#     url = pw.CharField()
#     game_desc = pw.ForeignKeyField(Game_Description)
#
#     class Meta:
#         database = db
#
# class Game_logo(pw.Model):
#     url = pw.CharField()
#     game_desc = pw.ForeignKeyField(Game_Description)
#     class Meta:
#         database = db
# db.connect()
# db.create_table(Genre)
# db.create_table(Games_Urls)
# db.create_table(Game_Description)
# db.create_table(Game_picture)
# db.create_table(Game_image)
# db.create_table(Game_logo)
# db.create_tables(Genre, Games_Urls, Game_Description, Game_picture, Game_image, Game_logo)
