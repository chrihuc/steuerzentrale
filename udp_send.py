# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:35:24 2016

@author: chuckle
"""

import socket

HOST = '127.0.0.1'   # Symbolic name meaning the local host
PORT = 5005    # Arbitrary non-privileged port
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command = raw_input('Enter your command: ')
    s.connect((HOST,PORT))
    if command.split(' ',1)[0]=='STORE':
        while True:
            additional_text = raw_input()
            command = command+'\n'+additional_text
            if additional_text=='.':
                break
    s.send(command)
    reply = s.recv(1024)
    if reply==command:
        print "Success"
    else:
        print reply
    s.close()