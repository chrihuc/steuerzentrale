#!  /usr/bin/python

import constants

import threading
#from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os, sys
#import urllib2
import xs1inputs, udpinputs, redundancy, periodic_sup
from alarmevents import alarm_event
import sqlsync

aes = alarm_event()
ssync = sqlsync.sync()

for table in ["Settings","Besucher","Bewohner","cron","gcm_users","Szenen","Wecker"]:
    try:
        ssync.export(table, "XS1DB")
        ssync.trunc_import(table, "XS1DB") 
        aes.new_event(description="Success sync "+table, prio=0)
    except:
        aes.new_event(description="Error sync "+table, prio=0)

threadliste = []

t = threading.Thread(target=xs1inputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=udpinputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=redundancy.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=periodic_sup.main, args = [])
threadliste.append(t)
t.start()

#print threadliste
#add supervision of threads

try:
    while constants.run:
        for t in threadliste:
            if not t in threading.enumerate():
                constants.run = False
                sys.exit() 
        time.sleep(1)
except KeyboardInterrupt:
    constants.run = False
    sys.exit() 
 
    
