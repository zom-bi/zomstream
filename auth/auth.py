#!/usr/bin/env python

# imports
# http server
import http.server
import socketserver

import urllib
import re
import sys
import signal
import os
from urllib.parse import urlparse, parse_qs

if os.environ['password']:
  password = os.environ['password']
else:
  print("missing password environment variable.") 
  sys.exit(1)

listenport = 8080

def sigterm_handler(_signo, _stack_frame):
    httpd.socket.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def log(text):
    sys.stdout.write(str(text)+'\n')
    sys.stdout.flush()

class handlers(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # send 200 to every request so auth gets a ok for now.
        query_components = parse_qs(urlparse(self.path).query)
        log("Passkey = " + str(query_components['pass'][0]))
        if query_components['pass'][0] == password:
            self.send_response(200)
        else:
            self.send_response(403)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(bytes('ok.', "utf-8"))
    def do_HEAD(self):
        self.do_GET()
try:
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", listenport), handlers)
    httpd.serve_forever()

except KeyboardInterrupt:
    httpd.socket.close()
    sys.exit(0)

