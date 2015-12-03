#!  /usr/bin/python

import constants

import threading
#from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os, sys
#import urllib2
import xs1inputs, udpinputs, redundancy, periodic_sup
from alarmevents import alarm_event
import sqlsync

#delay for changeover
time.sleep(10)

aes = alarm_event()
ssync = sqlsync.sync()

syncliste = []
syncliste += ["Settings"]
syncliste += ["Besucher"]
syncliste += ["Bewohner"]
syncliste += ["cron"]
syncliste += ["gcm_users"]
#syncliste += ["Szenen"]
syncliste += ["Wecker"]
for table in syncliste:
    try:
        ssync.export(table, "XS1DB")
        ssync.trunc_import(table, "XS1DB") 
        aes.new_event(description="Success sync "+table, prio=0)
    except:
        aes.new_event(description="Error sync "+table, prio=0)

threadliste = []

t = threading.Thread(name="xs1", target=xs1inputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="udp",target=udpinputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="redun",target=redundancy.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="peri",target=periodic_sup.periodic_supervision, args = [])
threadliste.append(t)
t.start()

#print threadliste
#add supervision of threads

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
 
    
