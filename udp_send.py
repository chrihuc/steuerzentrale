# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:35:24 2016

@author: chuckle
"""

import socket

HOST = '192.168.192.10'   # Symbolic name meaning the local host
PORT = 5005    # Arbitrary non-privileged port
if False:
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
        
if False:
    dicti = {}
    dicti['Value'] = 'Test'
    dicti['Name'] = 0
    hbtsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    hbtsocket.sendto(str(dicti),(HOST,5000))     
    
if True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command = {'Command':'Update'}
    s.connect((HOST,PORT))
#    if command.split(' ',1)[0]=='STORE':
#        while True:
#            additional_text = raw_input()
#            command = command+'\n'+additional_text
#            if additional_text=='.':
#                break
    s.send(str(command))
    reply = s.recv(1024)
    if reply==command:
        print "Success"
    else:
        print reply
    s.close()    