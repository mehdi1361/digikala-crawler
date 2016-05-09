from farsroid_db import Games_Urls
from game_page import game_crawl
fetch_game_page = Games_Urls.select()

for game in fetch_game_page:
    print 'id=%s, url=%s' % (game.id,game.url)
    game_crawl.delay(game.url, game.id)
