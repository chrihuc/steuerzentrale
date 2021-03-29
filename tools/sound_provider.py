#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:41:56 2017

@author: christoph
"""

import os
import time
from threading import Thread
import constants
from tools import toolbox

from socketserver import TCPServer

try:
    # python 2
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
except ImportError:
    # python 3
    from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        while constants.run:
            self.handle_request()

def main():
    port = constants.sound_prov.PORT
    web_dir = os.path.join(os.path.abspath(os.curdir), 'media')
    httpd = HTTPServer(web_dir, ("", port))
#    httpd.serve_forever()
    httpd.serve_forever()
    print('Stopping Soundprovider')
    httpd.socket.close()

#
#class HttpServer(Thread):
#    """A simple HTTP Server in its own thread"""
#
#    def __init__(self, port):
#        super(HttpServer, self).__init__()
#        self.daemon = True
#        handler = SimpleHTTPRequestHandler
#        self.httpd = TCPServer(("", port), handler)
#
#    def run(self):
#        """Start the server"""
#        print('Start HTTP server')
#        self.httpd.serve_forever()
#
#    def stop(self):
#        """Stop the server"""
#        print('Stop HTTP server')
#        self.httpd.socket.close()
#
#def main():
#    # Settings
#    port = constants.sound_prov.PORT
#    os.chdir("./media")
#    server = HttpServer(port)
#    server.start()
#    time.sleep(10**8)
#    server.stop()
    
#main()