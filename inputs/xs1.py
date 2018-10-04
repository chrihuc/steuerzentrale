#!/usr/bin/env python

import constants

import pycurl, os

from threading import Timer
import time
import sys
from time import localtime,strftime

from alarm_event_messaging import alarmevents as aevs
from database import mysql_connector as msqc
from tools import toolbox
from outputs import xs1
from outputs import szenen

#toolbox.log('debug on')

# TODO: unittest?

selfsupervision = True

aes = aevs.AES()
conn = pycurl.Curl()
last_data = ""
ezcontrol = xs1.XS1(constants.xs1_.IP)
conn = pycurl.Curl()
#scenes = szenen.Szenen()

def last_data_reset():
    last_data = ""

def on_receive(data):
    data = data.decode()
    if not constants.run:
        conn.close()
        sys.exit("Error message")
    global heartbeat
    global last_data
    global ldt
    if False:
        ldt.cancel()
        ldt = Timer(1, last_data_reset)
        ldt.start()
        if last_data == data:
            return
    count = int(msqc.setting_r("NumRestart"))
    if count > 0:
        msqc.setting_s("NumRestart", str(0))
    if count > 1:
        aes.new_event(description="XS1 wieder erreichbar", prio=3)
        msqc.setting_s("XS1_off", "inactive")
#Zerlegung des Empfangs
    toolbox.log(data)
    value = float(data.split(" ")[-1])
    name = 'XS1.' + str(data.split(" ")[-3])
    #now = datetime.datetime.now().strftime("%H:%M:%S.%f")
    #aes.new_event(description="Empfangen: " + name + " " + str(now), prio=0)
#####################
#Heartbeat & Server Steuerung
#####################
    if (("heartbeat" in name) and (value == 0)):
        heartbeat.cancel()
        heartbeat = Timer(constants.heartbt, heartbeat_sup)
        heartbeat.start()
        ezcontrol.SetSwitchFunction("heartbeat", "1")
    szenen.Szenen.trigger_scenes(name, value)
#    szns, desc = msqc.inputs(name,value)
#    for szene in szns:
#        if szene <> None:
#            scenes.threadExecute(szene, check_bedingung=False, wert=value, device=desc)
    last_data = data

def heartbeat_sup():
  if selfsupervision:
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    msqc.setting_s("Autorestart", str(now))
    count = int(msqc.setting_r("NumRestart"))
    if count == 0:
        aes.new_event(description="Verbindung unterbrochen XS1inputs", prio=1)
    if ((count > 0) and (msqc.setting_r("XS1_off") == "inactive")):
        aes.new_event(description="XS1 nicht erreichbar", prio=2)
        msqc.setting_s("XS1_off", "Active")
    msqc.setting_s("NumRestart", str(count + 1))
    exectext = "sudo killall python"
    print("XS1 connection lost")
    if toolbox.ping(constants.router_IP):
        conn.close()
        sys.exit("XS1 goodbye")
        #os.system(exectext)
    else:
        reset_wlan()
        sys.exit("XS1 goodbye")
        #os.system(exectext)

def reset_wlan():
    os.system('sudo ifdown --force wlan0')
    os.system('sudo ifup wlan0')


def main():
    global heartbeat
    global ldt
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    msqc.setting_s("Laststart", str(now))
    if selfsupervision:
        while not toolbox.ping(constants.router_IP):
            #reset_wlan()
            time.sleep(60)
    heartbeat = Timer(constants.heartbt, heartbeat_sup)
    heartbeat.start()
    ezcontrol.SetSwitchFunction("heartbeat", "1")
    ldt = Timer(2, last_data_reset)

    conn.setopt(pycurl.URL, constants.xs1_.STREAM_URL)
    conn.setopt(pycurl.WRITEFUNCTION, on_receive)
    #aes.new_event(description="XS1inputs neugestartet", prio=0)
    conn.perform()


if __name__ == '__main__':
    main()
