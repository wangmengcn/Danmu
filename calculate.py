# -*- coding: UTF-8 -*-
# 用以统计火箭分布信息
from pymongo import MongoClient
import pymongo
import time
import datetime

cli = MongoClient(host="123.206.211.77")
db = cli["Douyu"]
col = db["rocket"]

senderrows = col.find()
recverrows = col.find()
timerows = col.find()
senders = {}
recvers = {}


def sortNames(data, key):
    sortdata = {}
    for rocket in data:
        senderkey = rocket[key].encode('utf-8')
        if senderkey not in sortdata.keys():
            sortdata[senderkey] = 1
        else:
            sortdata[senderkey] += 1
    sortsender = sorted(sortdata.iteritems(), key=lambda d: d[1], reverse=True)
    return sortsender


def giftTime(data):
    sortdate = {}
    for rocket in data:
        hour = time.strftime("%H", time.localtime(float(rocket["date"])))
        if str(hour) not in sortdate.keys():
            sortdate[str(hour)] = 1
        else:
            sortdate[str(hour)] += 1
        sortvalue = sorted(sortdate.iteritems(),
                           key=lambda d: d[1], reverse=True)
    return sortvalue

# 逐分钟获取🚀总量
def rocketTime():
    rockdata = col.find().sort([("date", pymongo.ASCENDING)])
    sortgift = {}
    keys = []
    for item in rockdata:
        giftTime = datetime.datetime.fromtimestamp(int(float(item["date"])))
        month = str(giftTime.month)
        day = str(giftTime.day)
        hour = str(giftTime.hour)
        minute = str(giftTime.minute)
        splash = "-"
        key = splash.join([month, day, hour, minute])

        if sortgift.get(key) == None:
            if len(keys) ==0:
                keys.append(key)
                sortgift[key] = 1
            else:
                count = sortgift[keys[len(keys) - 1]]
                sortgift[key] = count + 1
                keys.append(key)
        else:
            sortgift[key] += 1
    #sortgift = sorted(sortgift.iteritems(), key=lambda d: d[1], reverse=False)
    return sortgift
