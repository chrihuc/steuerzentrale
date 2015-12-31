#!/usr/bin/env python

import constants

import pycurl,httplib,xml,urllib2,subprocess,os
from classes import  ping
from mysql_con import setting_s, setting_r, inputs
from threading import Timer
import threading
import time
import sys
from time import localtime,strftime
from socket import socket, AF_INET, SOCK_DGRAM
#from szenen import set_szene
from alarmevents import alarm_event

selfsupervision = True

aes = alarm_event()
mySocket = socket( AF_INET, SOCK_DGRAM )
conn = pycurl.Curl()
last_data = ""

def last_data_reset():
    last_data = ""
            
def on_receive(data):
    if not constants.run:
        sys.exit("Error message")
    global heartbeat
    global last_data
    global ldt
    ldt.cancel()
    ldt = Timer(1, last_data_reset)
    ldt.start() 
    if last_data == data:
        return
    count = int(setting_r("NumRestart"))
    if count > 0:
        setting_s("NumRestart", str(0))
    if count > 1:
        aes.new_event(description="XS1 wieder erreichbar", prio=3)
        setting_s("XS1_off", "inactive")
#Zerlegung des Empfangs
    value = float(data.split(" ")[-1])
    name = str(data.split(" ")[-3])
    #now = datetime.datetime.now().strftime("%H:%M:%S.%f") 
    #aes.new_event(description="Empfangen: " + name + " " + str(now), prio=0)
#####################
#Heartbeat & Server Steuerung
#####################
    if (("heartbeat" == name) and (value == 0)):
        heartbeat.cancel()
        heartbeat = Timer(constants.heartbt, heartbeat_sup)
        heartbeat.start()        
        mySocket.sendto('heartbeat',(constants.udp_.IP,constants.udp_.PORT))  
    szns = inputs(name,value)
    last_data = data
    
def heartbeat_sup():
  if selfsupervision:
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))  
    setting_s("Autorestart", str(now))
    count = int(setting_r("NumRestart"))
    if count == 0:
        aes.new_event(description="Verbindung unterbrochen XS1inputs", prio=1)
    if ((count > 0) and (setting_r("XS1_off") == "inactive")):
        aes.new_event(description="XS1 nicht erreichbar", prio=2)
        setting_s("XS1_off", "Active")
    setting_s("NumRestart", str(count + 1))
    exectext = "sudo killall python"
    if ping(constants.router_IP):
        os.system(exectext)
    else:
        reset_wlan()
        os.system(exectext)   

def reset_wlan():
    os.system('sudo ifdown --force wlan0') 
    os.system('sudo ifup wlan0')


def main():  
    global heartbeat
    global ldt
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))  
    setting_s("Laststart", str(now))
    if selfsupervision:
        while not ping(constants.router_IP):
            #reset_wlan()
            time.sleep(60)        
    heartbeat = Timer(constants.heartbt, heartbeat_sup)
    heartbeat.start()
    ldt = Timer(2, last_data_reset)
    conn = pycurl.Curl()  
    conn.setopt(pycurl.URL, constants.xs1_.STREAM_URL)  
    conn.setopt(pycurl.WRITEFUNCTION, on_receive)
    aes.new_event(description="XS1inputs neugestartet", prio=0)
    conn.perform()

    
if __name__ == '__main__':
    main()    
