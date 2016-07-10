# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import time
from datetime import datetime
from datetime import time as dtime
from pymongo import MongoClient

HOST = "http://www.douyu.com"
Directory_url = "http://www.douyu.com/directory?isAjax=1"
SinglePage = "http://www.douyu.com/directory/game/LOL?page=1&isAjax=1"
Qurystr = "/?page=1&isAjax=1"

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
connection = "keep-alive"
CacheControl = "no-cache"
UpgradeInsecureRequests = 1
headers = {
    'User-Agent': agent,
    'Host': HOST,
    'Accept': accept,
    'Cache-Control': CacheControl,
    'Connection': connection,
    'Upgrade-InsecureRequests': UpgradeInsecureRequests
}

cli = MongoClient(host="123.206.211.77")
db = cli["Douyu"]
col = db["Roominfo"]


def get_roominfo(data):
    if data:
        firstpage = BeautifulSoup(data)
        roomlist = firstpage.select('li')
        print len(roomlist)
        if roomlist:
            for room in roomlist:
                try:
                    roomid = room["data-rid"]
                    roomtitle = room.a["title"]
                    roomtitle = roomtitle.encode('utf-8')
                    roomowner = room.select("p > span")
                    roomtag = room.select("div > span")
                    roomimg = room.a
                    roomtag = roomtag[0].string
                    date = datetime.now()
                    # now = datetime.datetime(
                    # date.year, date.month, date.day, date.hour, date.minute)
                    if len(roomowner) == 2:
                        zbname = roomowner[0].string
                        audience = roomowner[1].get_text()
                        audience = audience.encode('utf-8').decode('utf-8')
                        image = roomimg.span.img["data-original"]
                        word = u"万"
                        if word in audience:
                            r = re.compile(r'(\d+)(\.?)(\d*)')
                            data = r.match(audience).group(0)
                            audience = int(float(data) * 10000)
                        else:
                            audience = int(audience)
                        roominfo = {
                            "roomid": int(roomid),
                            "roomtitle": roomtitle,
                            "anchor": zbname,
                            "audience": audience,
                            "tag": roomtag,
                            "date": date,
                            "img" : image
                        }
                        col.insert_one(roominfo)
                    # print roomid,":",roomtitle
                except Exception, e:
                    pass


def insert_info():
    session = requests.session()
    pagecontent = session.get(Directory_url).text
    pagesoup = BeautifulSoup(pagecontent)
    games = pagesoup.select('a')
    col.drop()
    for game in games:
        links = game["href"]
        gameurl = HOST + links + Qurystr
        print gameurl
        gamedata = session.get(gameurl).text
        get_roominfo(gamedata)
# get_roominfo(pagecontent)

insert_info()
