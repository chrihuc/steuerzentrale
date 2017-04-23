# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:43:14 2016

@author: christoph
"""

import constants

from mysql_con import inputs, mdb_read_table_column, settings_r, mdb_set_table
from cmd_szenen import szenen
from cmd_cron import cron

from alarmevents import alarm_event
from messaging import messaging

import threading
import socket
import time
import sys
import json
import datetime

hostName = socket.gethostbyname( constants.eigene_IP )

biSocket = socket.socket()# socket.AF_INET, socket.SOCK_STREAM )
biSocket.bind( (hostName, constants.udp_.biPORT) )
biSocket.listen(5)

PORT_NUMBER = constants.udp_.PORT
broadSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
#broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadSocket.bind( (hostName, constants.udp_.broadPORT) )

borad_to_guis = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
borad_to_guis.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

scenes = szenen()
aes = alarm_event()
mes = messaging()
crn = cron()

SIZE = 1024

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

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
    elif ('Android_id' in data_ev):
        # aes.new_event('Register new Client: ' + data_ev.get('Name'))  
        mes.register_user(data_ev)
    elif ('Device' in data_ev) and ('Command' in data_ev):
        scenes.threadSetDevice(data_ev['Device'], data_ev['Command'])
    elif ('Request' in data_ev):
        if data_ev.get('Request') == 'Settings':
            data = str(settings_r())
        elif data_ev.get('Request') == 'Wecker':            
            data = json.dumps(crn.get_all(wecker=True), default=handler)
            print data
    elif ('SetWecker' in data_ev):
        table = constants.sql_tables.cron.name
        for entry in eval(data_ev['SetWecker']):
            device = entry['Name']
            mdb_set_table(table, device, entry)
    elif ('Log' in data_ev):
        borad_to_guis.sendto(str(data_ev),('192.168.192.255',5000))
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
            
        #conn.sendall(data)
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
            exec_data(data_ev, data)

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
