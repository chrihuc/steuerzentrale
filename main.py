#!  /usr/bin/python

import constants
from szn_timer import szenen_timer

import threading
#from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os, sys
#import urllib2
import inp_xs1, inp_cron, inp_udp #redundancy, 
from inp_inter import anwesenheit
from alarmevents import alarm_event
from mysql_con import setting_s
#import sqlsync

#delay for changeover
#time.sleep(10)

aes = alarm_event()
anw = anwesenheit()
#ssync = sqlsync.sync()
#
#syncliste = []
#syncliste += ["Settings"]
#syncliste += ["Besucher"]
#syncliste += ["Bewohner"]
##syncliste += ["cron"]
#syncliste += ["gcm_users"]
##syncliste += ["Szenen"]
#syncliste += ["Wecker"]
##syncliste += ["Sideboard"]
#for table in syncliste:
#    try:
#        ssync.export(table, "XS1DB")
#        ssync.trunc_import(table, "XS1DB") 
#        aes.new_event(description="Success sync "+table, prio=0)
#    except:
#        aes.new_event(description="Error sync "+table, prio=0)

# init
init_settings = {'V00WOH1SRA1DI01':1,'V00WOH1SRA1DI04':1,'V00WOH1SRA1DI05':1}
for setting in init_settings:
    setting_s(setting, init_settings[setting])


threadliste = []

t = threading.Thread(name="xs1", target=inp_xs1.main, args = [])
threadliste.append(t)
t.start()

#t = threading.Thread(name="udp",target=inp_udp.main, args = [])
#threadliste.append(t)
#t.start()

t = threading.Thread(name="udp.bidirekt", target=inp_udp.bidirekt, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="udp.broadcast", target=inp_udp.broadcast, args = [])
threadliste.append(t)
t.start()
#
#t = threading.Thread(name="redun",target=redundancy.main, args = [])
#threadliste.append(t)
#t.start()
#
t = threading.Thread(name="peri",target=inp_cron.periodic_supervision, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="anwesenheit",target=anw.check_handys_service, args = [])
threadliste.append(t)
t.start()

aes.new_event(description="All Threads started", prio=1)
#print threadliste
#add supervision of threads

try:
    while constants.run:
        for t in threadliste:
            if not t in threading.enumerate():
                aes.new_event(description="Thread stopped: "+t.name, prio=1)
                constants.run = False
                sys.exit() 
        time.sleep(10)
except KeyboardInterrupt:
    constants.run = False
sys.exit() 
 
    
