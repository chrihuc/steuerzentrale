#!  /usr/bin/python


from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()
aes.new_event(description="Starting", prio=9)

import threading
import time, sys
import os
import argparse

import constants

from inputs import cron
#from inputs import udp_listener
from inputs import xs1
from inputs import internal
from outputs import temp_control

from tifo import tf_connection

from database import mysql_connector as msqc



from tools import sound_provider as sp
from tools import toolbox
#toolbox.log('debug on')



anw = internal.Anwesenheit()

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', type=int, nargs='?', help='debug', default=0)
parser.add_argument('-m', '--module', nargs='?', help='debug', default='')
parser.add_argument('-p', '--passive', nargs='?', help='debug')

args = parser.parse_args()

if getattr(args, 'debug') > 0:
    constants.debug = True
    constants.debug_level = getattr(args, 'debug')
if getattr(args, 'module') != '':
    constants.debug_text = getattr(args, 'module')
if getattr(args, 'passive') is not None:
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

#services = {'xs1':xs1.main}


t = toolbox.OwnTimer(0, function=xs1.main, args = [], name="xs1")
threadliste.append(t)
t.start()

for tf_con in constants.tifo:
    tifo_inst = tf_connection.TiFo(tf_con)
    t = toolbox.OwnTimer(0, function=tifo_inst.main, args = [], name="TiFo" + tf_con)
    threadliste.append(t)
    t.start()

t = toolbox.OwnTimer(0, function=temp_control.TempController.start, args = [], name="TempCTRL")
threadliste.append(t)
t.start()

t = toolbox.OwnTimer(0, function=cron.periodic_supervision, args = [], name="cron")
threadliste.append(t)
t.start()

t = toolbox.OwnTimer(0, function=anw.check_handys_service, args = [], name="anwesenheit")
threadliste.append(t)
t.start()

t = toolbox.OwnTimer(0, function=sp.main, args = [], name="sound_prov")
threadliste.append(t)
t.start()

from outputs import batswitch
t = toolbox.OwnTimer(0, function=batswitch.main, args = [], name="mqtt_batswitch")
threadliste.append(t)
t.start()

from inputs import mqtt_client
t = toolbox.OwnTimer(0, function=mqtt_client.main, args = [], name="mqtt_inputs")
threadliste.append(t)
t.start()

from secvest import secvest_handler
t = toolbox.OwnTimer(0, function=secvest_handler.main, args = [], name="secvest")
threadliste.append(t)
t.start()

try:
    from inputs import owm
    t = toolbox.OwnTimer(0, function=owm.main, args = [], name="weather")
    threadliste.append(t)
    t.start()
except:
    aes.new_event(description="OWM not installed", prio=9)

import app
t = toolbox.OwnTimer(0, function=app.main, args = [], name="flask")
threadliste.append(t)
t.start()

if constants.debug:
    toolbox.log(threadliste)

startup = True
time.sleep(5)
#add supervision of threads
aes.new_event(description="All Threads kicked off", prio=9)

try:
    while constants.run:
        allgut = True
        for t in threadliste:
            if not t in threading.enumerate():
                allgut = False
                if not t.failed:
                    if t.restartCounter == 2:                    
                        aes.new_event(description="Thread stopped: "+t.name, prio=9)
                    t.failed = True
                try:
                    new_t = toolbox.OwnTimer(0, name=t.name, function=t.function, args = t.args)
                    new_t.start()
                    new_t.failed = True
                    new_t.restartCounter = t.restartCounter + 1
                    threadliste.remove(t)
                    threadliste.append(new_t)
                    aes.new_event(description="Restarted Thread: "+t.name, prio=1)
                except:
                    aes.new_event(description="Couldn't restart Thread "+t.name+", killing python", prio=9)
                    toolbox.restart()
            else:
                if t.failed:
                    if t.restartCounter >= 2:
                        aes.new_event(description="Thread running again: "+t.name, prio=9)
                    t.failed = False
                    t.restartCounter = 0
        if startup and allgut:
            startup = False
            aes.new_event(description="All Threads runnung", prio=9)
            toolbox.log('threads running')
        toolbox.sleep(10)
except KeyboardInterrupt:
    constants.run = False
    time.sleep(5)
    for t in threadliste:
        if t in threading.enumerate():
            print(t.name + ' still running')
sys.exit()


