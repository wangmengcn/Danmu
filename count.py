# -*- coding: utf-8 -*-
# 实时获取数据库中信息，并返回给前端
from http.server import BaseHTTPRequestHandler, HTTPServer
import calculate
import json

PORT_NUMBER = 7000


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'json/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        value = calculate.rocketTime()
        self.wfile.write(json.dumps(value))
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port', PORT_NUMBER)
    server.serve_forever()
except Exception, e:
    pass
