# -*- coding: utf-8 -*-
# 实时获取数据库中信息，并返回给前端
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import json

PORT_NUMBER = 8000
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
        self.wfile.write(rocket)
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port', PORT_NUMBER

    server.serve_forever()
except Exception, e:
    pass
