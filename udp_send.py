# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:35:24 2016

@author: chuckle
"""

import socket

HOST = '192.168.192.25'   # Symbolic name meaning the local host
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
        
if True:
    dicti = {}
    #dicti['Value'] = 'Test'
    dicti['Command'] = 'Update'
    hbtsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    hbtsocket.sendto(str(dicti),(HOST,5005))     
    
if True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #command = {'Command':'Update'}
    data_ev = {}
    data_ev['Device'] = 'V00WOH1SRA1LI03'
    data_ev['red'] = 0L
    data_ev['green'] = 0
    data_ev['blue'] = 0
    s.connect((HOST,PORT))
#    if command.split(' ',1)[0]=='STORE':
#        while True:
#            additional_text = raw_input()
#            command = command+'\n'+additional_text
#            if additional_text=='.':
#                break
    s.send(str(data_ev))
    reply = s.recv(1024)
    if reply==command:
        print "Success"
    else:
        print reply
    s.close()    