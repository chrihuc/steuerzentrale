#!  /usr/bin/python



import threading
import time, sys
import os

import constants

from inputs import cron
from inputs import udp_listener
from inputs import xs1
from inputs import internal

from database import mysql_connector as msqc

from alarm_event_messaging import alarmevents as aevs

from tools import sound_provider as sp
from tools import toolbox
#toolbox.log('debug on')

aes = aevs.AES()
anw = internal.Anwesenheit()


if sys.argv:
    if 'debug' in sys.argv:
        toolbox.log('debug on')
        constants.debug = True
        if '1' in sys.argv:
            constants.debug_level = 1
    if 'passive' in sys.argv:
        toolbox.log('passive on')
        constants.passive = True

# init
init_settings = {'V00WOH1SRA1DI01':1,'V00WOH1SRA1DI04':1,'V00WOH1SRA1DI05':1}
for setting in init_settings:
    msqc.setting_s(setting, init_settings[setting])

def start_bokeh():
    cmd = 'bokeh serve --address=192.168.192.10 --port=5050 --allow-websocket-origin=192.168.*.*:5050 bokeh/server.py'
    os.system(cmd)

threadliste = []

t = threading.Thread(name="xs1", target=xs1.main, args = [])
threadliste.append(t)
t.start()

#t = threading.Thread(name="udp",target=inp_udp.main, args = [])
#threadliste.append(t)
#t.start()

t = threading.Thread(name="udp.bidirekt", target=udp_listener.bidirekt, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="udp.broadcast", target=udp_listener.broadcast, args = [])
threadliste.append(t)
t.start()
#
#t = threading.Thread(name="redun",target=redundancy.main, args = [])
#threadliste.append(t)
#t.start()
#
t = threading.Thread(name="peri",target=cron.periodic_supervision, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(name="anwesenheit",target=anw.check_handys_service, args = [])
threadliste.append(t)
t.start()

# start_bokeh()

t = threading.Thread(name="sound_prov",target=sp.main, args = [])
threadliste.append(t)
t.start()

aes.new_event(description="All Threads started", prio=1)
if constants.debug:
    toolbox.log(threadliste)

#add supervision of threads
toolbox.log('threads running')

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
 
    
