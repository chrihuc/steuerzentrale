#!  /usr/bin/python


from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()
aes.new_event(description="Starting", prio=7)

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
from outputs import batswitch
from inputs import mqtt_client

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

t = toolbox.OwnTimer(0, function=batswitch.main, args = [], name="mqtt_batswitch")
threadliste.append(t)
t.start()

t = toolbox.OwnTimer(0, function=mqtt_client.main, args = [], name="mqtt_inputs")
threadliste.append(t)
t.start()

aes.new_event(description="All Threads started", prio=7)
if constants.debug:
    toolbox.log(threadliste)

#add supervision of threads
toolbox.log('threads running')

try:
    while constants.run:
        for t in threadliste:
            if not t in threading.enumerate():
                aes.new_event(description="Thread stopped: "+t.name, prio=1)
                try:
                    new_t = toolbox.OwnTimer(0, name=t.name, function=t.function, args = t.args)
                    new_t.start()
                    threadliste.remove(t)
                    threadliste.append(new_t)
                    aes.new_event(description="Restarted Thread: "+t.name, prio=7)
                except:
                    constants.run = False
                    aes.new_event(description="Couldn't restart Thread "+t.name+", killing python", prio=7)
                    exectext = "sudo killall python3"
                    os.system(exectext)
                    sys.exit()
        toolbox.sleep(10)
except KeyboardInterrupt:
    constants.run = False
    time.sleep(5)
    for t in threadliste:
        if t in threading.enumerate():
            print(t.name + ' still running')
sys.exit()


