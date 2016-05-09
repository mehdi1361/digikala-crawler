
import urllib2
import json
from bs4 import BeautifulSoup
from farsroid_db import Games_Urls, Genre
from game_page import insert_game_url
gens = Genre.select()
for gen in gens:
    try:
        for i in range(1,100):
            url = '%s%s/' % (gen.genre_url, i)
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            text = resp.read().decode('utf-8')
            soup = BeautifulSoup(text)
            soup = soup.find_all(attrs={'class': 'post-bot row'})
            for link in soup:
                insert_game_url.delay(link.a.get('title'), link.a.get('href'), gen.id)
                print link.a.get('title')
                print link.a.get('href')
    except:
        print 'end of genre'
