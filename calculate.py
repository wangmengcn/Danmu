#-*- coding: UTF-8 -*-
# 用以统计火箭分布信息
from pymongo import MongoClient
import time

cli = MongoClient()
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
        hour = time.strftime("%H",time.localtime(float(rocket["date"])))
        print hour
        if str(hour) not in sortdate.keys():
            sortdate[str(hour)] = 1
        else:
            sortdate[str(hour)] += 1
        sortvalue = sorted(sortdate.iteritems(),
                           key=lambda d: d[1], reverse=True)
    return sortvalue

sortsender = sortNames(senderrows, "sender_id")
sortrecver = sortNames(recverrows, "recver_id")
sorthour = giftTime(timerows)

for item in sorthour:
	print item
