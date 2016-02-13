#!/usr/bin/env python

import constants

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
#from socket import error as socket_error
#from socket import socket, AF_INET, SOCK_DGRAM
import sys
from cmd_sonos import sonos
#from samspy import remotecontrol
from classes import myezcontrol, ping
import os
import time
from time import localtime,strftime
#from datetime import date
import threading
from threading import Timer
#import re
#import csv
import MySQLdb as mdb
from phue import Bridge
#from get_next_alarm import get_wecker
##mail
#from email.mime.text import MIMEText
#from subprocess import Popen, PIPE
from mysql_con import mdb_sonos_r, mdb_sonos_s, setting_s, setting_r, mdb_szene_r, mdb_marantz_r, mdb_marantz_s, mdb_fern_r_neu, mdb_sideb_r, app_r, mdb_hue_s, mdb_sideb_s
from szenen import set_szene, sonos_set_szene, tv_set_szene, set_TF_LEDs, hue_set_szene, set_TF_LEDs
from messaging import messaging
from alarmevents import alarm_event
#from text_to_sonos import downloadAudioFile
from tablecontrol import tablecontrol

########################
#Variablen declarification
########################

aes = alarm_event()
if not (ping('192.168.192.190')):
    aes.new_event(description="Hue nicht erreichbar", prio=2)
if not (ping('192.168.192.4')):
    aes.new_event(description="XS1 nicht erreichbar", prio=2)        

ezcontrol = myezcontrol(constants.xs1_.IP,constants.xs1_.USER,constants.xs1_.PASS)

PORT_NUMBER = 5000
SIZE = 1024

no_event_list = ["Toggle_Kueche","TV_Channel_up","TV_Channel_down","Marantz_leiser","Marantz_lauter"]

tc = tablecontrol()

hostName = gethostbyname( constants.eigene_IP )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, constants.UDP_PORT) )
IRSocket = socket( AF_INET, SOCK_DGRAM )
sn=sonos()
RaspBMC = socket( AF_INET, SOCK_DGRAM )
gbl_test = 1
heller = False
dimm_wz = False
dimm_esz = False
alarm_steh = False
TV_eingeschaltet = False
Amp_eingeschaltet = False

heartbt = 130

hbridge = Bridge(constants.hue_.IP)

message = messaging()
aes = alarm_event()

###################
#Marantz
###################         

def set_auto_szene():
    time.sleep(2)
    if (setting_r("AV_cmd")<>"1"):
        szene = mdb_marantz_r("Aktuell")
        if str(szene.get("Power")) == "False":
            pass
            #set_szene("auto_szene_Aus")
        elif (mdb_marantz_r('Aktuell').get('Source') <> mdb_marantz_r(str(setting_r("Kommando"))).get('Source')):
            if str(szene.get("Source")) == "11":
                set_szene("auto_szene_TV")
                setting_s("Kommando", "TV")
            elif str(szene.get("Source")) == "22":
                set_szene("auto_szene_PS3")
                setting_s("Kommando", "PS3")
            elif str(szene.get("Source")) == "99":
                set_szene("auto_szene_RaspBMC")
                setting_s("Kommando", "RaspBMC")
                time.sleep(5)
                ezcontrol.SetSwitch("RaspberryPi", str(100))
                ezcontrol.SetSwitch("RaspberryPi", str(100))
            elif str(szene.get("Source")) == "CC":
                set_szene("auto_szene_Sonos")
                setting_s("Kommando", "Sonos")
    #time.sleep(2)       
    #setting_s("AV_cmd", "0")

        
###################
#Hauptszenen
###################
def Alles_ein():
    global V_A_aus_del
    t = threading.Thread(target=set_szene, args=["Alles_ein"])
    t.start()
    aes.check_liste() 
           
###################
# Lese Bewohner und Besucher
################### 
        
def read_mysql(table):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    liste = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + table
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        j = 0
        for row in results:
            for i in range (0,len(row)):
                dicti[field_names[i]] = row[i]
            liste.append(dicti)
            dicti = {}
            j = j + 1
    con.close()
    return liste        

def write_mysql(table, name, setting, wert, prod):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'UPDATE '+ table +' SET ' + str(setting) + ' = "' + str(wert) + '", prod = "' + str(prod) + '" WHERE Name = "'+ str(name) + '"'
        cur.execute(sql)
    con.close()

def read_bebe_action(BeBe, Status, Event):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    liste = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM KeyActions where BeBe = "' + str(BeBe) + '" AND Status = "' + str(Status) + '" AND Event = "' + str(Event) + '"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        j = 0
        for row in results:
            for i in range (0,len(row)):
                dicti[field_names[i]] = row[i]
            liste.append(dicti)
            dicti = {}
            j = j + 1
    con.close()
    return liste    
    
###################
#receive and select    
###################
def restart_services_h():
    zeit =  time.time()
    now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))  
    setting_s("Autorestart", str(now))
    count = int(setting_r("NumRestart"))
    if count == 0:
        aes.new_event(description="Verbindung unterbrochen", prio=1)
    if ((count > 0) and (setting_r("XS1_off") == "inactive")):
        aes.new_event(description="XS1 nicht erreichbar", prio=2)
        setting_s("XS1_off", "Active")
    setting_s("NumRestart", str(count + 1))    
    exectext = "sudo killall python"
    os.system(exectext)
    
def main():
    asz = Timer(2, set_auto_szene)
    heartbeat = Timer(heartbt, restart_services_h)
    heartbeat.start()
    ezcontrol.SetSwitchFunction("heartbeat", str(1))
    ezcontrol.SetSwitchFunction("NotbetrNot", str(1))
    #Initialize scenes
    if ((setting_r("Status") == "Am Gehen 1") or (setting_r("Status") == "Am Gehen 2")):
        t = threading.Thread(target=set_szene, args=["Alles_aus_4"])
        t.start()
    if ((setting_r("Status") == "Am Gehen 3") or (setting_r("Status") == "Gegangen") or (setting_r("Status") == "Urlaub")):
        t = threading.Thread(target=set_szene, args=["Alles_aus_4"])
        t.start()
    if ((setting_r("Status") == "Abwesend") or (setting_r("Status") == "Urlaub")):
        t = threading.Thread(target=set_szene, args=["Alles_aus_5"])
        t.start()    
    if ((setting_r("Status") == "Schlafen")):
        t = threading.Thread(target=set_szene, args=["sz_Schlafen_stealth"])
        t.start()    

    aes.new_event(description="Outputs neugestartet", prio=0)
    while constants.run:
            (data,addr) = mySocket.recvfrom(SIZE)
            heartbeat.cancel()
            heartbeat = Timer(heartbt, restart_services_h)
            heartbeat.start() 
            isdict = False
            #if True:
            try:
                data_ev = eval(data)
                if type(data_ev) is dict:
                    if "Source" in data_ev:
                        #threading hinzufuegen ansonsten timed es aus
                        asz.cancel()
                        mdb_marantz_s("Aktuell", data_ev)
                        asz = Timer(2, set_auto_szene)
                        #asz.start()
                    elif "Key" in data_ev: 
                        gefunden = False
                        aes.new_event(description="Schluessel: "+str(data_ev.get("Key")), prio=0)
                        for typ in ["Bewohner", "Besucher"]:
                            namen = read_mysql(typ)
                            for name in namen:
                                if (str(data_ev.get("Key")) == name.get("USB_ID")) and (name.get("USB_State")>-15):
                                    aes.new_event(description=str(name.get("Name"))+" Schluessel: "+str(data_ev.get("value")), prio=0)
                                    gefunden = True
                                    try:
                                        actions = read_bebe_action(BeBe=typ, Status=setting_r("Status"), Event=data_ev.get("value"))
                                        t = threading.Thread(target=set_szene, args=[actions[0].get("Szene")])
                                        t.start()
                                    except:
                                        pass
                                    write_mysql(table=typ, name=str(name.get("Name")), setting="USB_State",wert=data_ev.get("value"), prod=data_ev.get("prod"))   
                        if not gefunden:
                            t = threading.Thread(target=set_szene, args=["FalscherSchluessel"])
                            t.start()                        
                    elif "Licht" in data_ev:
                        if str(data_ev.get("Licht")) in ["Stablampe 1","Stehlampe","Monaco Lampe","Balkonlampe","LightStrips 2","BettSabina","BettChris","SchlafziFenster"]:
                            #setting = {'hue': hue, 'bri': bri, 'sat': sat, 'an': an}
                            mdb_hue_s("App", data_ev)
                            hue_set_szene(str(data_ev.get("Licht")),"App")
                        else:
                            mdb_sideb_s("App", data_ev)
                            set_TF_LEDs(data_ev.get("Licht"), "App")
                    elif ("name" in data_ev) and ("value" in data_ev):
                        XS1DB = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
                        zeit =  time.time()
                        now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))                     
                        with XS1DB:
                            cur = XS1DB.cursor()
                            insertstatement = 'INSERT INTO Actuators(Name, Value, Date) VALUES("' + str(data_ev.get("name")) + '", ' + str(data_ev.get("value")) + ', "' + str(now) + '")'
                            cur.execute(insertstatement)   
                        XS1DB.close() 
                        szenen = tc.get_szene(sensor = data_ev.get("name"), value = data_ev.get("value"))
                        for szene in szenen:
                            t = threading.Thread(target=set_szene, args=[szene])
                            t.start()
                        if data_ev.get("name") == "Helligkeit":
                            setting_s("Helligkeit", str(data_ev.get("value"))) 
                        if data_ev.get("name") == "Haustuer":
                            setting_s("Haustuer", str(data_ev.get("value"))) 
                        if data_ev.get("name") == "SchlafZiFenster":
                            setting_s("SchlafZiFenster", str(data_ev.get("value")))                          
                    isdict = True
            except Exception as serr:
                isdict = False
            if (data == "heartbeat"):         
                ezcontrol.SetSwitchFunction("heartbeat", str(1))
                ezcontrol.SetSwitchFunction("NotbetrNot", str(1))
            else:
                if (not (data in no_event_list)) and (not (isdict)):
                    aes.new_event("UDP receive: "+data, karenz = 1)
            if "sz_" in data:
                t = threading.Thread(target=set_szene, args=[data])
                t.start()
            if "appz_" in data:
                t = threading.Thread(target=set_szene, args=[data[5:]])
                t.start()            
            if "az_" in data:
                t = threading.Thread(target=set_szene, args=[data])
                t.start()        
    #Hauptszenen
        #Alles ein
            if (data == "Alles_ein"):
                t = threading.Thread(target=set_szene, args=["Alles_ein"])
                t.start()
                if (setting_r("Status") == "Wach"):
                    t = threading.Thread(target=set_szene, args=["sz_gemuetlich"])
                    t.start()            
            elif (data == "Alles_ein_Flur"):
                ezcontrol.SetSwitch("Diele", str(100))
                t = threading.Thread(target=set_szene, args=["Alles_ein"])
                t.start()
                if (setting_r("Status") == "Wach"):
                    t = threading.Thread(target=set_szene, args=["sz_gemuetlich"])
                    t.start()   
        #app szenen
            elif "app_" in data:
                t = threading.Thread(target=set_szene, args=[str(app_r(data))])
                t.start()  
        #Wach
            elif (data == "Wach"):
                ezcontrol.SetSwitch("Kueche", str(100))
                t = threading.Thread(target=set_szene, args=["Wach"])
                t.start()
            elif (data == "Alles_aus_nochmal"):
                setting_s("Status", "Abwesend")
                ezcontrol.SetSwitch("Webcams", str(100))
                ezcontrol.SetSwitch("Anwesend_Block", str(0))
        #Schlafen
            elif (data == "Schlafen"):
                t = threading.Thread(target=set_szene, args=["Schlafen1"])
                t.start()
        #Alles aus
            elif (data == "Alles_aus"):
                Alles_aus()  
    #Mediaquellen            
        #Fernsehen$
            elif (data == "Media_TV"):
                t = threading.Thread(target=set_szene, args=["TV"])
                t.start()
        #Sonos        
            elif (data == "Media_Sonos"):
                t = threading.Thread(target=set_szene, args=["MediaSonos"])
                t.start()                                         
    #Serversteuerung funzt nicht
            elif (data == "Neustart_services"):
                exectext = "sudo killall python"
                os.system(exectext)     
            elif (data == "Neustart_raspberry"):
                os.system("sudo reboot")
            elif (data == "SonosWrite"):
                SonosWriteConfig()
    #temp_alar,       
            elif (data == "alle_alarme_gesehen"):
                aes.acknowledge_all()       
    #FernBett
            elif (data == "Bett_0_kurz"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_0_kurz"))
            elif (data == "Bett_0_lang"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_0_lang"))
            elif (data == "Bett_0_lang_lang"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_0_lang_lang"))           
            elif (data == "Bett_3_kurz"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_3_kurz"))
            elif (data == "Bett_3_lang"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_3_lang"))         
            elif (data == "Bett_4_kurz"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_4_kurz"))
            elif (data == "Bett_4_lang"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_4_lang"))
            elif (data == "Bett_7_kurz"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_7_kurz"))
            elif (data == "Bett_7_lang"):
                set_szene(mdb_fern_r_neu("Fern_Bett", "Fern_Bett", "Fern_Bett_7_lang"))  
            if "Distance_" in data:
                volume = (int(data.split("_")[1]) - 124) / 15 + 5
                sn.SetVolume(sn.SchlafZi, volume)
    sys.exit()

if __name__ == '__main__':
    main() 

