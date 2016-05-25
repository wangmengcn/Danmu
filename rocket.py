#-*- coding: UTF-8 -*-
import socket
import time
import re
from pymongo import MongoClient


'''这里要注意几个变量： host port roomid gid '''

HOST = '124.95.174.146'
PORT = 8601
RID = 319721
LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5" + \
    "/password@=1234567890123456/roomid@="+str(RID) + "/"
JION_GROUP = "type@=joingroup/rid@="+str(RID) + "/gid@=-9999" + "/"
ROOM_ID = "type@=qrl/rid@="+str(RID) + "/"
KEEP_ALIVE = "type@=keeplive/tick@=" + \
    str(int(time.time())) + "/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/"


def tranMsg(content):
    length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
    code = length
    magic = bytearray([0xb1, 0x02, 0x00, 0x00])
    end = bytearray([0x00])
    trscont = bytes(content.encode('utf-8'))
    return bytes(length + code + magic + trscont + end)


# 获取全频道播放的火箭信息
def get_rocket(data):
    try:
        sender_id = re.search('\/sn@=(.+?)\/', data).group(1)
        recver_id = re.search('\/dn@=(.+?)\/', data).group(1)
        recver_room = re.search('\/drid@=(.+?)\/', data).group(1)
        gift = re.search('\/gn@=(.+?)\/', data).group(1)
        rocketmsg = {}
        rocketmsg["sender_id"] = sender_id
        rocketmsg["recver_id"] = recver_id
        rocketmsg["recver_room"] = recver_room
        rocketmsg["gift"] = gift
        rocketmsg["date"] = time.time()
        col.insert_one(rocketmsg, bypass_document_validation=False)
        print sender_id, "送给房间号为:", recver_room, "的", recver_id, "一个",\
            gift, "<", time.strftime(
                '%H-%I-%M', time.localtime(time.time())), ">"
    except Exception, e:
        print "error occur:", repr(data)
    finally:
        pass

# 获取聊天信息


def get_chatmsg(data):
    try:
        sender_id = re.search('\/nn@=(.+?)\/', data).group(1)
        sender_content = re.search('\/txt@=(.+?)\/', data).group(1)
        chatmsg = {}
        chatmsg["sender_id"] = sender_id
        chatmsg["content"] = sender_content
        chatmsg["date"] = time.time()
        chatcol.insert_one(chatmsg, bypass_document_validation=False)
        print sender_id, "said:", sender_content, "at:<", time.strftime('%H-%I-%M', time.localtime(time.time())), ">"
    except Exception, e:
        print "error occur:", repr(data)
    finally:
        pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(tranMsg(LOGIN_INFO))
s.sendall(tranMsg(JION_GROUP))


sendlive = 0
client = MongoClient()
db = client["Douyu"]
col = db["rocket"]
chatcol = db["chatmsg"]
print "已连接至数据库"
while True:
    if sendlive % 2 == 0:
        print "----------------------------------Keep Alive----------------------------------"
        try:
            s.sendall(tranMsg(KEEP_ALIVE))
        except Exception, e:
            raise e
    sendlive += 1
    print sendlive
    try:
        data = s.recv(1000)
        if data:
            strdata = repr(data)
            if "type@=spbc" in strdata:
                get_rocket(data)
            if "type@=chatmsg" in strdata:
                get_chatmsg(data)
    except Exception, e:
        raise e
    time.sleep(1)

# s.close()
