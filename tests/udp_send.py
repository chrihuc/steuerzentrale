#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 21:42:20 2017

@author: christoph
"""

import socket

HOST = '192.168.192.10'   # Symbolic name meaning the local host
#PORT = 5005


dicti = {}
dicti['Device'] = 'Vm1ZIM1RUM1DO01'
dicti['Command'] = 'Aus'
hbtsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
hbtsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
hbtsocket.sendto(str(dicti),(HOST,5000)) 