# -*- coding: utf-8 -*-
# 实时获取数据库中信息，并返回给前端
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import json
from serverEnd import dataSender

PORT_NUMBER = 8888
client = MongoClient(host="123.206.211.77")
db = client["Douyu"]
col = db["rocket"]
msgcol = db["chatmsg"]


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'json/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        rocket = col.count()
        msg = msgcol.count()
        value = {
            "rocket": rocket,
            "msg": msg
        }
        name = dataSender.name
        value = dataSender.value
        result = {}
        times = 0
        while times < len(name):
            result[bytes(name[times],'UTF-8')] = value[times]
            times += 1
        self.wfile.write(json.dumps(result))
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port', PORT_NUMBER)
    server.serve_forever()
except Exception:
    pass
