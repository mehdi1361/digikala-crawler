#!/usr/bin/python2.7
import urllib3
import requests
import json
from bs4 import BeautifulSoup
from farsroid_db import Games_Urls, Game_Description, Game_picture
from celery import Celery

app = Celery('bazinama', broker='amqp://guest@localhost//')


@app.task
def insert_game_url(title, url, genre):
    game_url = Games_Urls(title=title, url=url, genre= genre)
    game_url.save()

@app.task
def insert_game_db(title_game,logo_src, detail_game, apk_file,game_trailer, game_id):
    game_desc = Game_Description(title=title_game, avatar= logo_src, detail=detail_game, apk=apk_file, trailer=game_trailer, game= game_id)
    game_desc.save()
    download('logo',game_id,apk_file)
    download('apk',game_id,apk_file)

@app.task
def insert_game_picture(image_url,game):
    pic = Game_picture(url =image_url, game_desc=game)
    pic.save()
    download('image', game, image_url)

@app.task
def download(key,file_id,file_url):
    response = requests.get(file_url)
    local_file_url = "product_apk/%s.apk" % file_id
    if key == 'image':
        local_file_url = "product_image/%s.jpg" % file_id

    if key == 'logo':
        local_file_url = "product_logo/%s.png" % file_id

    if response.status_code == 200:
        f = open(local_file_url, 'wb')
        f.write(response.content)
        f.close()
# game_page = Games_Urls.select()

@app.task
def game_crawl(url, game_id):
    # url = 'http://www.farsroid.com/clash-of-clans/'
    req = requests.get(url)
    # resp = urllib3.urlopen(req)
    text = req.text
    # text = resp.read().decode('utf-8')
    soup = BeautifulSoup(text)
    soup = soup.find(attrs={'class': 'single-post row'})
    logo_src = soup.img['src']

    soup = soup.find(attrs={'class': 'single-post-content contentia row'})
    soup1 = soup.find_all('p')
    detail_game=''
    title_game=''
    counter = 1
    for pa in soup1:
        if counter==1:
            title_game += pa.text
        else:
            detail_game += '%s\n' % pa.text
        counter +=1
    soup = BeautifulSoup(text)
    soup = soup.find_all(attrs={'class': 'dl-links col'})
    apk_file = ''
    game_trailer = ''
    for link in soup:
        # print(link)
        apk_file= link.a.get('href')

    # print 'logo= %s' % logo_src
    # print  'title= %s' % title_game
    # print 'detail= %s'% detail_game
    # print 'apk= %s'% apk_file
    # game_desc = Game_Description(title=title_game, avatar= logo_src, detail=detail_game, apk=apk_file, trailer=game_trailer, game= game_id)
    # game_desc.save()

    soup = BeautifulSoup(text)
    soup = soup.find_all(attrs={'class': 'item'})
    game_desc = Game_Description(title=title_game, avatar= logo_src, detail=detail_game, apk=apk_file, trailer=game_trailer, game= game_id)
    game_desc.save()
    # download('logo',game_id,apk_file)
    # download('apk',game_id,apk_file)
    counter = 1
    # for img in soup:
    #     # print img.img['src']
    #     # download('image',pic_id ,img.img['src'])
    #     pic = Game_picture(url =img.img['src'], game_desc=game_desc)
    #     pic.save()
    #     counter += 1
