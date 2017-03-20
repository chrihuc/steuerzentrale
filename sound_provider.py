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

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer



class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, port):
        super(HttpServer, self).__init__()
        self.daemon = True
        handler = SimpleHTTPRequestHandler
        self.httpd = TCPServer(("", port), handler)

    def run(self):
        """Start the server"""
        print('Start HTTP server')
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        print('Stop HTTP server')
        self.httpd.socket.close()

def main():
    # Settings
    port = constants.sound_prov.PORT
    os.chdir("./media")
    server = HttpServer(port)
    server.start()
    time.sleep(10**8)
    server.stop()
    
main()