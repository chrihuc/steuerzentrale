# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:43:14 2016

@author: christoph
"""

import constants

from mysql_con import inputs, mdb_read_table_column, settings_r
from cmd_szenen import szenen
import cmd_internal
from alarmevents import alarm_event

import threading
import socket
import time
import sys

hostName = socket.gethostbyname( constants.eigene_IP )

biSocket = socket.socket()# socket.AF_INET, socket.SOCK_STREAM )
biSocket.bind( (hostName, constants.udp_.biPORT) )
biSocket.listen(5)

PORT_NUMBER = constants.udp_.PORT
broadSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
broadSocket.bind( (hostName, constants.udp_.broadPORT) )
scenes = szenen()
aes = alarm_event()

SIZE = 1024

def exec_data(data_ev, data):
    if ('Name' in data_ev) and ('Value' in data_ev):
        name = data_ev.get('Name')
        value = data_ev.get('Value')
#        print name, value
        szns = inputs(name,value)
        for szene in szns:
            if szene <> None:
                scenes.threadExecute(szene, check_bedingung=False, wert = value)  
#    elif data_ev.get('Command')=='Update':
#        aes.new_event(description="System update", prio=0)
#        cmd_internal.git_update() 
    elif ('Szene' in data_ev):   
        name = data_ev.get('Szene') 
        if name in mdb_read_table_column(constants.sql_tables.szenen.name, 'Name'):
            scenes.threadExecute(name) 
    elif ('GCM-Client' in data_ev):
        aes.new_event('GCM Client: ' + data_ev.get('GCM-Client'))  
    elif ('Request' in data_ev):
        if data_ev.get('Request') == 'Settings':
            data = str(settings_r())
    return data              

def bidirekt():
    while constants.run:
        conn, addr = biSocket.accept()
        data = conn.recv(1024)
        print data
        if not data:
            break
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
        except Exception as serr:
            isdict = False
        if isdict:
            data = exec_data(data_ev, data)
        conn.send(data)
        conn.close()  

def broadcast():
    while constants.run:
        (data,addr) = broadSocket.recvfrom(SIZE)
        print data
        if not data:
            break
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
        except Exception as serr:
            isdict = False  
        if isdict:
            #print data_ev
            exec_data(data_ev)

def main():
    constants.run = True
    threadliste = []
    
    t = threading.Thread(name="bidirekt", target=bidirekt, args = [])
    threadliste.append(t)
    t.start()
    
    t = threading.Thread(name="broadcast", target=broadcast, args = [])
    threadliste.append(t)
    t.start()    
    
    try:
        while constants.run:
            for t in threadliste:
                if not t in threading.enumerate():
                    print t.name
                    constants.run = False
                    sys.exit() 
            time.sleep(10)
    except KeyboardInterrupt:
        constants.run = False
        sys.exit()    

if __name__ == '__main__': 
    main()