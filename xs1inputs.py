#!/usr/bin/env python

import constants

import pycurl,httplib,xml,urllib2,subprocess,os
#from urllib2 import URLError
from classes import  ping #myezcontrol,
from mysql_con import setting_s, setting_r, mdb_fern_r
from threading import Timer
import threading
import time
import sys
from time import localtime,strftime
#from datetime import date
#import datetime
from Sonos2Py import sonos
import MySQLdb as mdb
#import re
from socket import socket, AF_INET, SOCK_DGRAM
from szenen import set_szene
from alarmevents import alarm_event
#from sensor_health import check_sensor_health
#from periodic_sup import periodic_supervision
#from messaging import messaging
#from tinkerforge_class import TiFo_moist
#from balkon import balkon
from tablecontrol import tablecontrol
#from tuer_check import tuer_check
from heizung import temp_derivator

selfsupervision = True

aes = alarm_event()
tc = tablecontrol()
sn = sonos()
wohnT = temp_derivator("Wohnzimmer_T")
balkT = temp_derivator("Balkon_T")
XS1DB = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
#ezcontrol = myezcontrol(constants.xs1_.IP,constants.xs1_.USER,constants.xs1_.PASS)
mySocket = socket( AF_INET, SOCK_DGRAM )
conn = pycurl.Curl()

            
def on_receive(data):
    if not constants.run:
        sys.exit("Error message")
    global heartbeat
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
    if (("Neustart" == name) and (value == 0)):
        mySocket.sendto('Neustart_raspberry',(constants.udp_.IP,constants.udp_.PORT))         
    if (("Neustart" == name) and (value == 100)):
        mySocket.sendto('Neustart_services',(constants.udp_.IP,constants.udp_.PORT)) 
#####################
#tablecontrol
##################### 
    szenen = tc.get_szene(sensor = name, value = value)
    for szene in szenen:
        t = threading.Thread(target=set_szene, args=[szene])
        t.start()  
#####################
#Zeitschalter
##################### 
    if (("Beleuchtung_abends" == name) and (value == 100)):
        setting_s("Beleuchtung", "Abends")
        t = threading.Thread(target=set_szene, args=["sz_AbendBelEin"])
        t.start()            
    if (("Beleuchtung_abends" == name) and (value == 0)):
        setting_s("Beleuchtung", "Aus")
        if str(setting_r("Status")) <> "Wach":
            t = threading.Thread(target=set_szene, args=["sz_AbendBelAus"])
            t.start()        
    if (("Beleuchtung_morgens" == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=["sz_MorgenBelEin"])
        t.start()     
        setting_s("Beleuchtung", "Morgens")
    if (("Beleuchtung_morgens" == name) and (value == 0)):    
        setting_s("Beleuchtung", "Aus")
        t = threading.Thread(target=set_szene, args=["sz_MorgenBelAus"])
        t.start()         
#####################
#Schalter in dem Flur/Wohnzimmer / Normale Abwesenheit
#####################
    if (("Wand_Haupt_1" == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_1")])
        t.start()
    if (("Wand_Haupt_1" == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_2")])
        t.start()        
    if (("Wand_Haupt_2" == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_3")])
        t.start()
    if (("Wand_Haupt_2" == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_4")])
        t.start() 
    if (("Wand_Haupt_3" == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_5")])
        t.start()        
    if (("Wand_Haupt_4" == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_7")])
        t.start()
    if (("Wand_Haupt_4" == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Haupt", "Fern_Haupt_8")])
        t.start()         
#####################
#Schalter in dem Flur 2
#####################
    if (('Wand_Flur_5' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Flur", "Fern_Flur_1")])
        t.start()
    if (('Wand_Flur_5' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Flur", "Fern_Flur_2")])
        t.start()
    if (('Wand_Flur_7' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Flur", "Fern_Flur_3")])
        t.start() 
    if (('Wand_Flur_7' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Flur", "Fern_Flur_4")])
        t.start()           
#####################
#Schalter im Esszimmer
#####################
    if (('Wand_Wohnzi_1' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Esszi", "Fern_Esszi_1")])
        t.start()
    if (('Wand_Wohnzi_1' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Esszi", "Fern_Esszi_2")])
        t.start()
    if (('Wand_Wohnzi_3' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Esszi", "Fern_Esszi_3")])
        t.start() 
    if (('Wand_Wohnzi_3' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Esszi", "Fern_Esszi_4")]) 
        t.start()
##################
#Abwesend fall back
##################
    if (("Anwesend_Block" == name) and (value == 0)):
        if (setting_r("Status") == "Am Gehen 1") or (setting_r("Status") == "Am Gehen 2") or (setting_r("Status") == "Am Gehen 3"):
            mySocket.sendto('Alles_aus_nochmal',(constants.udp_.IP,constants.udp_.PORT))       
##################
#Reduit & Saugstauber
##################
    if (('Reduit_1' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Reduit", "Fern_Reduit_1")])
        t.start()
    if (('Reduit_1' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Reduit", "Fern_Reduit_2")])
        t.start()
    if (('Reduit_3' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Reduit", "Fern_Reduit_3")])
        t.start() 
    if (('Reduit_3' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Reduit", "Fern_Reduit_4")])
        t.start() 
    if (('Saugstauber' == name) and (value == 100)):
        mySocket.sendto('saugen',(constants.udp_.IP,constants.udp_.PORT))
##################
#Fernbedienung im Schlafzi
##################
#start stop of sonos player in bedroom
    if (('Fern_Schlafzi_1' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_1")])
        t.start()
    if (('Fern_Schlafzi_1' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_2")])
        t.start()
    if (('Fern_Schlafzi_2' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_3")])
        t.start() 
    if (('Fern_Schlafzi_2' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_4")])
        t.start() 
    if (('Fern_Schlafzi_3' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_5")])
        t.start()
    if (('Fern_Schlafzi_3' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_6")])
        t.start()
    if (('Fern_Schlafzi_4' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_7")])
        t.start()       
    if (('Fern_Schlafzi_4' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Schlafzi", "Fern_Schlafzi_8")])
        t.start()
##################
#Fernbedienung im Bad
################## 
    if (('Fern_Bad_1' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_1")])
        t.start()
    if (('Fern_Bad_1' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_2")])
        t.start()
    if (('Fern_Bad_2' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_3")])
        t.start() 
    if (('Fern_Bad_2' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_4")])
        t.start() 
    if (('Fern_Bad_3' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_5")])
        t.start()
    if (('Fern_Bad_3' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_6")])
        t.start()
    if (('Fern_Bad_4' == name) and (value == 100)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_7")])
        t.start()       
    if (('Fern_Bad_4' == name) and (value == 0)):
        t = threading.Thread(target=set_szene, args=[mdb_fern_r("Fern_Bad", "Fern_Bad_8")])
        t.start()
##################
# Fernbedienung Kueche
##################
    if (('Fern_Kuche_2' == name) and (value == 100)):
        mySocket.sendto('Media_TV',(constants.udp_.IP,constants.udp_.PORT))
    if (('Fern_Kuche_2' == name) and (value == 0)):
        mySocket.sendto('Mediarack_aus',(constants.udp_.IP,constants.udp_.PORT))
    if (('Fern_Kuche_3' == name) and (value == 100)):
        mySocket.sendto('TV_Channel_up',(constants.udp_.IP,constants.udp_.PORT))
    if (('Fern_Kuche_3' == name) and (value == 0)):
        mySocket.sendto('TV_Channel_down',(constants.udp_.IP,constants.udp_.PORT))
    if (('Fern_Kuche_4' == name) and (value == 100)):
        mySocket.sendto('Marantz_lauter',(constants.udp_.IP,constants.udp_.PORT))
    if (('Fern_Kuche_4' == name) and (value == 0)):
        mySocket.sendto('Marantz_leiser',(constants.udp_.IP,constants.udp_.PORT))
##################
# Fernbedienung Buero1
##################
    if (('Fern_Buero_1' == name) and (value == 100)):
        mySocket.sendto('scan1',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_1' == name) and (value == 0)):
        mySocket.sendto('scan2',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_2' == name) and (value == 100)):
        mySocket.sendto('scan3',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_2' == name) and (value == 0)):
        mySocket.sendto('scan4',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_3' == name) and (value == 100)):
        mySocket.sendto('scan5',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_3' == name) and (value == 0)):
        mySocket.sendto('scan6',(constants.scanner_.IP,constants.scanner_.PORT))   
    if (('Fern_Buero_4' == name) and (value == 100)):
        mySocket.sendto('scan7',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_4' == name) and (value == 0)):
        mySocket.sendto('scan8',(constants.scanner_.IP,constants.scanner_.PORT)) 
    if (('Fern_Buero_5' == name) and (value == 100)):
        mySocket.sendto('scan9',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_5' == name) and (value == 0)):
        mySocket.sendto('scan10',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_6' == name) and (value == 100)):
        mySocket.sendto('scan11',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_6' == name) and (value == 0)):
        mySocket.sendto('scan12',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_7' == name) and (value == 100)):
        mySocket.sendto('scan13',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_7' == name) and (value == 0)):
        mySocket.sendto('scan14',(constants.scanner_.IP,constants.scanner_.PORT))   
    if (('Fern_Buero_8' == name) and (value == 100)):
        mySocket.sendto('scan15',(constants.scanner_.IP,constants.scanner_.PORT))
    if (('Fern_Buero_8' == name) and (value == 0)):
        mySocket.sendto('scan16',(constants.scanner_.IP,constants.scanner_.PORT))         
##################
#Anruf und Nachricht
##################
    if (('eingehend_anruf' == name) and (value == 100)):
        mySocket.sendto('Incoming_call',(constants.udp_.IP,constants.udp_.PORT))
    if (('eingehend_nach' == name) and (value == 100)):
        mySocket.sendto('Incoming_mess',(constants.udp_.IP,constants.udp_.PORT))
##################
#Rauchmelder
##################
    if (('WonziRauchm' == name) and (value == 100)):
        aes.new_event(description="Feueralarm", prio=4.1)
    if (('WonziRauchm' == name) and (value == 0)):
        aes.new_event(description="Feueralarm aufgehoben", prio=4.3)        
##################
#Test
##################
    if (('Test' == name) and (value == 100)):
        aes.new_event(description="Test", prio=2.1, durchsage="Dies ist ein Testalarm", karenz=0)
        #mySocket.sendto('Test1',(constants.udp_.IP,constants.udp_.PORT))
    if (('Test' == name) and (value == 0)):
        mySocket.sendto('Test0',(constants.udp_.IP,constants.udp_.PORT))      
    # write to sql
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
    if ('Temperatur_Schlafzi' == name):
        setting_s("Temperatur_Schlafzi", str(value))
        if (value < int(setting_r("TempAlarmSchlafzi"))):
            aes.new_event(description="Schlafzimmer wird kalt", prio=2.2)
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Schlafzimmer_T(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)            
    elif ('Luftfeuchte_Schlafz' == name):
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Schlafzimmer_H(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)
    elif ('Temperatur_Wohnzi' == name):
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Wohnzimmer_T(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)          
        setting_s("Temperatur_Wohnzi", str(value))
        RolAvg =  wohnT.get_avg("Value",13)
        wohnT.write_data("RolAvg",RolAvg)
        D60 = RolAvg - wohnT.get_hist_value("RolAvg",60)
        D30 = RolAvg - wohnT.get_hist_value("RolAvg",30)
        D15 = RolAvg - wohnT.get_hist_value("RolAvg",15)
        wohnT.write_data("D3",D60)
        wohnT.write_data("D2",D30)
        wohnT.write_data("D1",D15)            
    elif ('Luftfeuchte_Wohnzi' == name):
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Wohnzimmer_H(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)   
    elif ('Temperatur_Balkon' == name):
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Balkon_T(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)  
        RolAvg =  balkT.get_avg("Value",30)
        balkT.write_data("RolAvg",RolAvg)
        D60 = RolAvg - balkT.get_hist_value("RolAvg",1440)
        D30 = RolAvg - balkT.get_hist_value("RolAvg",360)
        D15 = RolAvg - balkT.get_hist_value("RolAvg",180)
        balkT.write_data("D3",D60)
        balkT.write_data("D2",D30)
        balkT.write_data("D1",D15)         
    elif ('Luftfeuchte_Balkon' == name):
        with XS1DB:
            cur = XS1DB.cursor()
            insertstatement = 'INSERT INTO Balkon_H(Value, Date) VALUES(' + str(value) + ', "' + str(now) + '")'
            cur.execute(insertstatement)  
    elif ('_v' in data):    
        pass
    else:
        if (name != 'Steuerwert') and (name != 'heartbeat') and ((name != 'NotbetrNot') and (name != 'Notbetrieb')):
            with XS1DB:
               cur = XS1DB.cursor()
               insertstatement = 'INSERT INTO Actuators(Name, Value, Date) VALUES("' + str(name) + '", ' + str(value) + ', "' + str(now) + '")'
               cur.execute(insertstatement)      
#####################
#Balkontuer
#####################
    if setting_r("Fenster_override") == "Aus":
        if ('Balkontuer' == name):
            setting_s("Balkontuer", str(value))
        if ('Kuechentuer' == name): 
            setting_s("Kuechentuer", str(value))
    
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
  
def to_mysql(moisture):
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit))) 
    with XS1DB:
        cur = XS1DB.cursor()
        insertstatement = 'INSERT INTO Moisture(Value, Date) VALUES(' + str(moisture) + ', "' + str(now) + '")'
        cur.execute(insertstatement)  

def main():  
    global heartbeat
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))  
    setting_s("Laststart", str(now))
    if selfsupervision:
        while not ping(constants.router_IP):
            #reset_wlan()
            time.sleep(60)        
            
    heartbeat = Timer(constants.heartbt, heartbeat_sup)
    heartbeat.start()

    conn = pycurl.Curl()  
    conn.setopt(pycurl.URL, constants.xs1_.STREAM_URL)  
    conn.setopt(pycurl.WRITEFUNCTION, on_receive)
    aes.new_event(description="XS1inputs neugestartet", prio=0)
    conn.perform()

    
if __name__ == '__main__':
    main()    
