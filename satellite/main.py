#!/usr/bin/env python

import threading
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os
import urllib2
import tf_class

SERVER_IP_1   = '192.168.192.10'
SERVER_IP_2   = '192.168.192.33'
OUTPUTS_PORT = 5000

PORT_NUMBER = 5010
hostName = gethostbyname( '192.168.192.33' )
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )
SIZE = 1024

def send_heartbeat():
    while True:
        dicti = {}
        dicti['value'] = str(1)
        dicti['name'] = 'BueroPi'
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT))  
        time.sleep(60)

vc = tf_class.TiFo()

#tuer = tuer_switch()
#t = threading.Thread(target=tuer.monitor, args = [])
#t.start()

hb = threading.Thread(target=send_heartbeat, args = [])
hb.start()

while True:
    (data,addr) = mySocket.recvfrom(SIZE)
    isdict = False
    try:
        data_ev = eval(data)
        if type(data_ev) is dict:
            isdict = True
    except Exception as serr:
        isdict = False                