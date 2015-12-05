#!/usr/bin/env python

import constants

from Sonos2Py import sonos
from classes import myezcontrol, ping
import MySQLdb as mdb
from mysql_con import mdb_fern_r, mdb_sonos_r, mdb_sonos_s, mdb_szene_r, mdb_hue_r, setting_s, setting_r, settings_r, mdb_marantz_r, mdb_hue_s, mdb_fern_schluessel_r, mdb_sideb_r, mdb_ls_sz_r, hue_autolicht, mdb_tspled_r, mdb_get_dicti
import mysql_con
import time
from socket import socket, AF_INET, SOCK_DGRAM
from socket import error as socket_error
from phue import Bridge
import threading
from threading import Timer
from alarmevents import alarm_event
from samspy import remotecontrol
from text_to_sonos import downloadAudioFile
from time import localtime,strftime
from datetime import datetime
import datetime
from messaging import messaging
from cron import cron
#from cloudftp import get_serialnumbers
from webcammov import send_wc_pix
import os
from anwesenheit import anwesenheit
import satellites
#from plexapi.server import PlexServer

sn=sonos()
aes = alarm_event()
anw_status = anwesenheit()
mes = messaging()
crn = cron()

PS3_IP = '192.168.192.27'
BettPi_PIP = '192.168.192.24'

ezcontrol_status = {'Kueche':'Licht_Kueche'}
sonos_devices = {'SonosWohnZi':sn.WohnZi,'SonosKueche':sn.Kueche,'SonosBad':sn.Bad,'SonosSchlafZi':sn.SchlafZi}
sonos_zonen = {str(sn.WohnZi):sn.WohnZiZone,str(sn.Kueche):sn.KuecheZone,str(sn.Bad):sn.BadZone,str(sn.SchlafZi):sn.SchlafZiZone}
sonos_ezcont = {str(sn.WohnZi):'Sonos_Wohnzi',str(sn.Kueche):'Sonos_Kueche',str(sn.Bad):'Sonos_Bad',str(sn.SchlafZi):'Sonos_Schlafzi'}
schluessellist = {'Christoph':'C86000BDB9E9EE10800000B0','Sabina':'6CF049E0FBE2FD40B95F273B', 'Huckle':'00D0C9CCDE48EDB14000F139','Russ':'C86000BDB9F2EE10AA310081'}
sonos_szenen = {str(sn.WohnZi):'WohnZi',str(sn.Kueche):'Kueche',str(sn.Bad):'Bad',str(sn.SchlafZi):'SchlafZi'}
ezcont_interlock = {'Video_Audio':PS3_IP, 'BettPi':BettPi_PIP, 'Sonos_Wohnzi':PS3_IP, sn.WohnZi:PS3_IP}

tv_remote = remotecontrol(constants.eigene_IP,'192.168.192.26','00:30:1b:a0:2f:05')
tv_remote_lan = remotecontrol(constants.eigene_IP,'192.168.192.29','00:30:1b:a0:2f:05')
no_event = ['Alarm','Achtung','Hinweis','Hue_Meldung','set_hinweis']

ezcontrol = myezcontrol(constants.xs1_.IP,constants.xs1_.USER,constants.xs1_.PASS)
hbridge = Bridge(constants.hue_.IP)

router = satellites.get_satellite("Router")
pies = satellites.get_satellites()

MARANTZ_IP   = '192.168.192.25'
MARANTZ_PORT = 5010
MarantzSocket = socket( AF_INET, SOCK_DGRAM )

BETT_IP   = '192.168.192.24'
BETT_PORT = 5000
BettSocket = socket( AF_INET, SOCK_DGRAM )

RaspBMC_IP   = '192.168.192.24'
PORT_NUMBER = 5000
RaspBMC = socket( AF_INET, SOCK_DGRAM )

TuerSPi_IP   = '192.168.192.32'
TuerSPi_sock = socket( AF_INET, SOCK_DGRAM )

#plex = PlexServer()

typ_dict = mdb_szene_r("Device_Typ")
ezcontrol_devices = []
TF_LEDs = []
hue_devices = []
setting = []
sat_names = []
for device in typ_dict:
    if typ_dict.get(device) == "EZControl":
        ezcontrol_devices.append(device)
    if typ_dict.get(device) == "TF_LEDs":
        TF_LEDs.append(device)
    if typ_dict.get(device) == "Hue":
        hue_devices.append(device)   
    if typ_dict.get(device) == "setting":
        setting.append(device)   
    if typ_dict.get(device) == "satellite":
        sat_names.append(device)        

def main():
    #mysql_con.set_automode(device="Stehlampe", mode="man")
    #xs1_set_szene(device="Wohnzimmer_Decke", szene="man")
    constants.redundancy_.master = True
    set_szene("SchlafZi_alles_an")
    #set_szene("Test")
    #sonos_read_szene(sonos_devices.get("SonosBad"), mdb_sonos_r("TextToSonos"))
    #test("Stehlampe")
    #deactivate_usb_keys()
    #sonos_write_szene(sn.Bad)
    

def autolicht(helligkeit, offset = 60, minimum = 0, maximum=160):    
    #helligkeit gemessene
    #offset startpunkt der beleuchtung
    #gradient steigung der beleuchtung
    #mindest kleinste beleuchtung
    if int(helligkeit) <= int(offset):
        bel_wert = float(minimum) - (float(helligkeit)-float(offset))*(int(maximum)-int(minimum))/int(offset)
    else:
        bel_wert=0
    return bel_wert

def deactivate_usb_keys():
    anw_status.deactivate_keys()
    
def sonos_write_szene(player):
    Pause = 0
    Radio = 0
    TitelNr = 0
    Sender = ""
    Time = ""
    MasterZone = "Own"
    Volume = "None"
    posinfo = sn.GetPositionInfo(player)
    pos = sn.GetPosition(player)
    transinfo = sn.GetTransportInfo(player)
    for zone in sn.Zones:
        if zone in posinfo:
            MasterZone = zone
    if MasterZone == "Own":
        if "PLAYING" in transinfo:
            Pause = 0
        else:
            Pause = 1
        if "file" in posinfo:
            Radio = 0
        else:
            Radio = 1
        antwort = posinfo
        pos1 = antwort.find ('<TrackURI>',0) #('*&quot;&gt;',0)
        pos2 = antwort.find ('</TrackURI>',0) #('&lt;/res&gt;&lt;r:',0)
        Sender = antwort [pos1+10:pos2]
        TitelNr = int(pos[0])
        Time = pos[1]
    Volume = sn.GetVolume(player)
    if player == sn.WohnZi:
        playern = "WohnZi"
        plnum = 33
    elif player == sn.Kueche:
        playern = "Kueche"
        plnum = 40
    elif player == sn.Bad:
        playern = "Bad"
        plnum = 34
    elif player == sn.SchlafZi:
        playern = "SchlafZi"
        plnum = 35
    else:
        playern = player
        plnum = 0
    sn.SaveList(player, "Bad", 34)
    mdb_sonos_s(player, Pause, Radio, Sender, TitelNr, Time, MasterZone, Volume)   

def sonos_write_szene_chris(player):
    Pause = 0
    Radio = 0
    TitelNr = 0
    Sender = ""
    Time = ""
    MasterZone = "Own"
    Volume = "None"
    posinfo = sn.GetPositionInfo(player)
    pos = sn.GetPosition(player)
    transinfo = sn.GetTransportInfo(player)
    for zone in sn.Zones:
        if zone in posinfo:
            MasterZone = zone
    if MasterZone == "Own":
        if "PLAYING" in transinfo:
            Pause = 0
        else:
            Pause = 1
        if "file" in posinfo:
            Radio = 0
        else:
            Radio = 1
        antwort = posinfo
        pos1 = antwort.find ('<TrackURI>',0) #('*&quot;&gt;',0)
        pos2 = antwort.find ('</TrackURI>',0) #('&lt;/res&gt;&lt;r:',0)
        Sender = antwort [pos1+10:pos2]
        TitelNr = int(pos[0])
        Time = pos[1]
    else:
        return
    Volume = sn.GetVolume(player)
    sn.SaveList(player, "Christ Aktuell", 51)
    mdb_sonos_s("ChrisAktuell", Pause, Radio, Sender, TitelNr, Time, MasterZone, Volume)    
    
def sonos_read_szene(player, sonos_szene, hergestellt = False):
    #read szene from Sonos DB and execute
    if str(sonos_szene.get('Volume')) <> 'None':
        sn.SetVolume(player, sonos_szene.get('Volume'))
    zone = sonos_szene.get('MasterZone')
    if (str(zone) <> "None") and (str(zone) <> "Own"):
        sn.CombineZones(player, zone)
    else:
        zoneown = sonos_zonen.get(str(player))
        if str(sonos_szene.get('Radio')) == '1':
            sn.setRadio(player, str(sonos_szene.get('Sender')))
        elif str(zone) <> "None":
            sn.ClearZones(player)
            sn.ClearList(player)
            sn.PlayListNr(player, str(sonos_szene.get('PlayListNr')))
            sn.ActivateList(player, zoneown)
            sn.Seek(player, "TRACK_NR", str(sonos_szene.get('TitelNr')))
            if str(sonos_szene.get('Time')) <> 'None':
                sn.Seek(player, "REL_TIME", sonos_szene.get('Time'))
        if (sonos_szene.get('Pause') == 1) or hergestellt:
            sn.SetPause(player)
        elif sonos_szene.get('Pause') == 0:
            sn.SetPlay(player)
    
def sonos_set_szene(player, szenen):
    #execute specific scenes, or go to sonos_read_szene
    try:
        if type(eval(str(szenen))) == list:
            pass
        else:
            szenen = [szenen]
    except NameError as serr:
        szenen = [szenen]        
    for szene in szenen:
        for anzahl in range(4):
            try:
                if str(szene) == "Pause":
                    sn.SetPause(player)
                elif str(szene) == "Play":
                    sn.SetPlay(player)                
                elif str(szene) == "Aus":
                    if ezcontrol.GetSwitch(sonos_ezcont.get(player)) > "0.0":
                        sonos_write_szene(player)
                        sn.SetPause(player)
                    if ezcont_interlock.get(player) <> None:
                        if ping(ezcont_interlock.get(player)):
                            aes.new_event(description="PS3 noch eingeschaltet", prio=1)
                        else:
                            ezcontrol.SetSwitch(sonos_ezcont.get(player), "0.0")
                    else:
                        ezcontrol.SetSwitch(sonos_ezcont.get(player), "0.0")
                elif str(szene) == "Save":
                    sonos_write_szene(player)  
                elif str(szene) == "SaveChris":
                    sonos_write_szene_chris(player)                  
                elif str(szene) == "Time":
                    sonos_write_szene(player)
                    lt = localtime()
                    stunde = int(strftime("%H", lt))
                    minute = int(strftime("%M", lt)) 
                    if (minute <> 0) and (minute <> 30):
                        text = "Es ist " + str(stunde) + " Uhr und " + str(minute) + " Minuten."
                        laenge = downloadAudioFile(text)
                        sonos_read_szene(player, mdb_sonos_r("TextToSonos"))
                        time.sleep(laenge + 1)            
                        sonos_read_szene(player, mdb_sonos_r(sonos_szenen.get(str(player))))
                elif str(szene) == "Durchsage":
                    sonos_write_szene(player)   
                    text = setting_r("Durchsage")        
                    laenge = downloadAudioFile(text)
                    sonos_read_szene(player, mdb_sonos_r("TextToSonos"))
                    time.sleep(laenge + 1)            
                    sonos_read_szene(player, mdb_sonos_r(sonos_szenen.get(str(player))))            
                elif str(szene) == "Return":
                    sonos_read_szene(player, mdb_sonos_r(sonos_szenen.get(str(player))), hergestellt = True)          
                elif ((str(szene) == "An") and (ezcontrol.GetSwitch(sonos_ezcont.get(player))== "0.0")):
                    ezcontrol.SetSwitch(sonos_ezcont.get(player), "100.0")
                elif ((str(szene) == "resume") and (ezcontrol.GetSwitch(sonos_ezcont.get(player))== "0.0")):
                    ezcontrol.SetSwitch(sonos_ezcont.get(player), "100.0")
                    time.sleep(60)
                    sonos_read_szene(player, mdb_sonos_r(sonos_szenen.get(str(player))))            
                elif (str(szene) == "lauter"):
                    ActVol = sn.GetVolume(player)
                    if ActVol >= 20: increment = 8
                    if ActVol < 20: increment = 8
                    if ActVol < 8: increment = 8
                    VOLUME = ActVol + increment 
                    sn.SetVolume(player, VOLUME)
                elif (str(szene) == "leiser"):
                    ActVol = sn.GetVolume(player)
                    if ActVol >= 20: increment = 8
                    if ActVol < 20: increment = 8
                    if ActVol < 8: increment = 8
                    VOLUME = ActVol - increment 
                    sn.SetVolume(player, VOLUME)
                elif (str(szene) == "inc_lauter"):
                    ActVol = sn.GetVolume(player)
                    if ActVol >= 20: increment = 8
                    if ActVol < 20: increment = 4
                    if ActVol < 8: increment = 2
                    VOLUME = ActVol + increment 
                    sn.SetVolume(player, VOLUME)
                elif (str(szene) == "inc_leiser"):
                    ActVol = sn.GetVolume(player)
                    if ActVol >= 20: increment = 8
                    if ActVol < 20: increment = 4
                    if ActVol < 8: increment = 2
                    VOLUME = ActVol - increment 
                    sn.SetVolume(player, VOLUME)                
                elif (str(szene) == "WeckerAnsage"):
                    sn.SetPause(player)
                    sn.SetVolume(player, 20)
                    setting_s("Durchsage", str(crn.next_wecker_heute_morgen()))
                    text = setting_r("Durchsage")        
                    laenge = downloadAudioFile(text)
                    sonos_read_szene(player, mdb_sonos_r("TextToSonos"))
                    time.sleep(laenge + 1)  
                    sn.SetPause(player)
                elif ((str(szene) <> "resume") and (str(szene) <> "An") and (str(szene) <> "None")):
                    sonos_szene = mdb_sonos_r(szene)
                    sonos_read_szene(player, sonos_szene)
                if "WeckerPhase" in str(szene) and str(player) == "SonosSchlafZi":
                    transinfo = sn.GetTransportInfo(player)
                    if "PLAYING" in transinfo or str(setting_r("Status")) <> "Wecken":
                        pass
                    else:
                        aes.new_event(description="Alternativer Wecker", prio=0)
                        if not ping(str(sn.SchlafZi), number = 2):
                            ezcontrol.SetSwitch(sonos_ezcont.get(player), "100.0")
                            time.sleep(30)
                        sonos_szene = mdb_sonos_r("Wecker2")
                        sonos_read_szene(player, sonos_szene)
                        time.sleep(5)
                        transinfo = sn.GetTransportInfo(player)
                        if "PLAYING" in transinfo or str(setting_r("Status")) <> "Wecken":
                            pass
                        else:
                            aes.new_event(description="Alternativer Wecker", prio=0)
                            if not ping(str(sn.SchlafZi), number = 2):
                                ezcontrol.SetSwitch(sonos_ezcont.get(player), "100.0")
                                time.sleep(30)
                            sonos_szene = mdb_sonos_r("WeckerAlternative")
                            sonos_read_szene(player, sonos_szene)                    
                break
            except socket_error as serr:
                ezcontrol.SetSwitch(sonos_ezcont.get(player), "100.0")
                time.sleep(10)                    

def RaspBMC_off():
    RaspBMC.sendto('PowerOff',(RaspBMC_IP,PORT_NUMBER))    
    Rasp_aus_del = Timer(60, xs1_set_szene, ['RaspberryPi','0'])
    Rasp_aus_del.start()

def dimmen(device):
    setting_s(device, "heller")
    while str(setting_r(device)) <> 'fixed':
        Helligkeit = ezcontrol.GetSwitch(device)
        if (Helligkeit == "100.0"):
            setting_s(device, "dunkler")
        elif (Helligkeit == "0.0"):
            setting_s(device, "heller")
        if str(setting_r(device)) == "heller":
            n_Helligkeit = str(float(Helligkeit)+10)
        else:
            n_Helligkeit = str(float(Helligkeit)-10)
        ezcontrol.SetSwitch(device, str((n_Helligkeit)))
        time.sleep(1.5)
        
def xs1_set_szene(device, szene):
    if szene in ["man", "auto"]:
        mysql_con.set_automode(device=device, mode=szene)
        return
    if (device == "Video_Audio") and str(szene) == "0":
        if ping(ezcont_interlock.get(device)):
            aes.new_event(description="PS3 noch eingeschaltet", prio=1)
            return
        while setting_r("AV_mode") <> "Aus":
        #if setting_r("AV_mode") <> "Aus":
            #return
            marantz_set_szene("Aus")
            time.sleep(20)
    elif (ezcont_interlock.get(device) <> None) and (str(szene) == "0"):
        if ping(ezcont_interlock.get(device)):
            if device == 'RaspberryPi':
                RaspBMC_off()
            else:
                aes.new_event(description="PS3 noch eingeschaltet", prio=1)
            return
    if szene == "dimmen":
        if str(setting_r(device)) <> 'fixed':
            setting_s(device, "fixed")
        else:
            dimmen(device)
        return
    if szene == str(-1):
        if ezcontrol.GetSwitch(str(device)) > "0.0":
            ezcontrol.SetSwitch(str(device), "0.0")
        else:
            ezcontrol.SetSwitch(str(device), "100.0")
    else:
        ezcontrol.SetSwitch(str(device), str(szene))
        if ezcontrol_status.get(str(device)) <> "":
            if str(szene) == "0.0":
                setting_s(ezcontrol_status.get(str(device)),"Aus")
            else:
                setting_s(ezcontrol_status.get(str(device)),"An")
    #now = datetime.datetime.now().strftime("%H:%M:%S.%f") 
    #aes.new_event(description="Versandt: " + str(now), prio=0)
                
def set_ls_schlafzi(szene):
    #deprecated
    if mdb_ls_sz_r(szene) <> {}:
        szene = mdb_ls_sz_r(szene)
    BettSocket.sendto(str(szene),(BETT_IP,BETT_PORT))

def send_cmd_satellite(device, szene):
    for item in pies:
        if item.name == str(device):
            command = mdb_get_dicti(str(item.command_set),szene)
            item.send_udp_cmd(command)
                
def hue_set_szene(device, szene):
    if szene in ["man", "auto"]:
        mysql_con.set_automode(device=device, mode=szene)
        return
    elif szene == 'Save': 
        hue = hbridge.get_light(device, 'hue')
        bri = hbridge.get_light(device, 'bri')
        sat = hbridge.get_light(device, 'sat')
        an = hbridge.get_light(device, 'on') 
        #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
        setting = {'hue': hue, 'bri': bri, 'sat': sat, 'an': an}
        mdb_hue_s(device, setting)
        return
    elif szene == 'toggle':
        an = hbridge.get_light(device, 'on') 
        if an:
            hbridge.set_light(device, {'on':False})
        else:
            hbridge.set_light(device, {'on':True}) 
        return
    elif szene == 'sz_toggle':
        an = hbridge.get_light(device, 'on') 
        if an:
            szene="SZ_Aus"
        else:
            hbridge.set_light(device, {'on':True})
            return      
    keys = ['bri', 'hue', 'sat', 'transitiontime']
    szene = mdb_hue_r(szene)
    if szene.get('bri') <> None:
        try:
            szene['bri'] = int(szene.get('bri'))
        except ValueError:
            auto_l_settings = hue_autolicht(szene.get('bri'))
            szene['bri'] = int(autolicht(helligkeit = setting_r("Helligkeit"), offset = auto_l_settings.get("offset"), minimum = auto_l_settings.get("min"), maximum=auto_l_settings.get("max")))   
            if szene.get('bri') < 1:
                szene['an'] =  0   
                szene['bri'] =  0
    if str(szene.get('an')) == "1" or str(szene.get('an')) == "True":
        hbridge.set_light(device, {'on':True}) 
        time.sleep(0.5)
    command = {}
    for key in keys:
        if ((szene.get(key) <> "") and (str(szene.get(key)) <> "None")):
            command[key] = szene.get(key)
    if command <> {}:
        hbridge.set_light(device, command)
    if str(szene.get('an')) == "0" or str(szene.get('an')) == "False":
        hbridge.set_light(device, {'on':False})  
    #now = datetime.datetime.now().strftime("%H:%M:%S.%f") 
    #aes.new_event(description="Versandt: " + str(now), prio=0)

def Tuer_auf():
    Anwesend_init = setting_r("Anwesenheit")
    if str(setting_r("Status")) in ["Schlafen", "Abwesend", "Urlaub"]:
        einbruch = True
        setting_s("Einbruch","True")
        set_szene("Einbruch_1")
        set_szene("Einbruch_Sofort")
        #setting_s("Status","Einbruch")
    else:
        einbruch = False
    #alle weggewesen     
    i = 0
    while i < 7:
        i = i + 1    
        akt_status = anw_status.check_all()
        if akt_status.get("Einbruch") == False:
            einbruch = False
            setting_s("Einbruch","False") 
            if str(setting_r("Status")) in ["Abwesend", "Urlaub"]: 
                set_szene("Heimgekommen")
            if str(setting_r("Status")) in ["Schlafen"]: 
                set_szene("einer_heimgekommen")                
            i = 60
        if str(setting_r("Status")) in ["Wach", "Besuch"]:
            einbruch = False
            setting_s("Einbruch","False") 
            i = 60  
        if Anwesend_init > akt_status.get("Anwesenheit"):
            aes.new_event(description="Jemand gegangen", prio=0)
            Anwesend_init = akt_status.get("Anwesenheit")
            #!!!!!!!!!!!!!achtung noch die passenden Szenen setzen
            #einer gegangen einer schlaeft check if this gets even executed then            
        time.sleep(10)
    #if einbruch:
    #    setting_s("Einbruch","True")
    #else:
    #    setting_s("Einbruch","False")
    if str(setting_r("Einbruch")) == "True":
        aes.new_event(description="Einbruch", prio=3.1)
        Tuer_auf()

def TuerSPi(szene):
    kommando = mdb_tspled_r(szene)
    TuerSPi_sock.sendto(str(kommando),(TuerSPi_IP,PORT_NUMBER))
    
def Schluessel_weg():
    anwesende = schluessel.anwesende()
    if anwesende == []:
        aes.new_event(description="Alle Schluessel weg", prio=0)    
        set_szene("Alles_aus_Schl")
    
def set_szene(name):
    global schlummern
    global bad_ir
    if str(name) == "None" or str(name) == "":
        return
    if "Tuer_auf" in str(name):
    #if str(name) == "Tuer_auf":
        t = threading.Thread(target=Tuer_auf)
        t.start()
    if str(name) == "Schluessel_weg":
        t = threading.Thread(target=Schluessel_weg)
        t.start()         
    szene = mdb_szene_r(name)
    if str(szene) == "{}": return
    no_list = ["Priority", "Beschreibung", "Status", "Durchsage"]
    bedingungen = {}
    erfuellt = True
    if str(szene.get("Bedingung")) <> "None":
        bedingungen = eval(szene.get("Bedingung"))    
        erfuellt = True
    settings = settings_r()
    for bedingung in bedingungen:
        try:
            groesser = bedingungen.get(bedingung).find('>')
            kleiner = bedingungen.get(bedingung).find('<')
            if groesser >-1 and kleiner >-1:
                schwelle_u = float(bedingungen.get(bedingung)[groesser+1:kleiner])
                if float(settings.get(bedingung)) <= schwelle_u:
                    erfuellt = False
                schwelle_o = float(bedingungen.get(bedingung)[kleiner+1:len(bedingungen.get(bedingung))])
                if float(settings.get(bedingung)) >= schwelle_o:
                    erfuellt = False    
            elif groesser >-1:
                schwelle = float(bedingungen.get(bedingung)[groesser+1:len(bedingungen.get(bedingung))])
                if float(settings.get(bedingung)) <= schwelle:
                    erfuellt = False                     
            elif kleiner >-1:
                schwelle = float(bedingungen.get(bedingung)[kleiner+1:len(bedingungen.get(bedingung))])
                if float(settings.get(bedingung)) >= schwelle:
                    erfuellt = False        
            else:
                if not(str(settings.get(bedingung)) in bedingungen.get(bedingung)):
                    erfuellt = False
        except Exception as e:
            if not(str(settings.get(bedingung)) in bedingungen.get(bedingung)):
                erfuellt = False 
    if str(szene.get("XS1_Bedingung")) <> "None" :
         xs1_bedingung = eval(szene.get("XS1_Bedingung"))
         if str(ezcontrol.GetSwitch(str(xs1_bedingung.keys()[0]))) <> str(xs1_bedingung[xs1_bedingung.keys()[0]]):
             erfuellt = False
    if not(name in no_event) and erfuellt:
        if str(szene.get("Beschreibung")) in ['None','']:
            aes.new_event(description="Szenen: " + name, prio=eval(szene.get("Priority")), karenz = 0.03)
        else:
            aes.new_event(description= str(szene.get("Beschreibung")), prio=eval(szene.get("Priority")), karenz = 0.03)
    if erfuellt:
        interlocks = {}
        if str(szene.get("Auto_Mode")) == "True":
            interlocks = mdb_szene_r("Auto_Mode")
        hue_count = 0
        hue_delay = 0
        if str(szene.get("Durchsage")) <> "None":
            setting_s("Durchsage", str(szene.get("Durchsage"))) 
        if ((szene.get("Amp") <> "") and (str(szene.get("Amp")) <> "None")):
            setting_s("AV_cmd", "1")
            setting_s("Kommando", str(szene.get("Amp")))
            delay = 20
            if mdb_marantz_r('Aktuell').get('Power') == "False":
                delay = 30
            mar_fb = Timer(delay, marantz_fb)
            #mar_fb.start() 
        if name in ["WeckerMute", "WeckerPhase1"] or "Schlummern" in name:
            schlummern.cancel()
        if name in ["Bad_ir"]:
            bad_ir.cancel()            
        for idk, key in enumerate(szene):        
            if ((szene.get(key) <> "") and (str(szene.get(key)) <> "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                if (type(szene.get(key)) == str) and (not(str(key) in no_list)):
                    try:
                        if type(eval(szene.get(key))) == list or type(eval(szene.get(key))) == dict:
                            kommandos = eval(szene.get(key))
                        else:
                            kommandos = [szene.get(key)]
                    except NameError as serr:
                        kommandos = [szene.get(key)]
                else:
                    kommandos = [szene.get(key)]
                if constants.redundancy_.master:
                    if key in ezcontrol_devices:
                        for kommando in kommandos:
                            t = threading.Thread(target=xs1_set_szene, args=[key, kommando])
                            t.start()
                    elif key == "set_Task":
                        for kommando in kommandos:
                            mes.send_direkt(to=mes.alle, titel="Setting", text=str(kommando))  
                    elif key == "set_Task_zuhause":
                        for kommando in kommandos:
                            mes.send_zuhause(to=mes.alle, titel="Setting", text=str(kommando))                          
                            #mes.send_direkt(mes.tf201,"Setting",str(kommando))                    
                    elif key in sonos_devices:
                        #for kommando in kommandos:
                        t = threading.Thread(target=sonos_set_szene, args=[sonos_devices.get(key), kommandos])
                        t.start()                
                    elif key in hue_devices:
                        for kommando in kommandos:
                            if hue_count > 1:
                                hue_delay += 0.75
                                hue_count = 0
                            hue_del = Timer(hue_delay, hue_set_szene, [key, kommando])
                            hue_del.start()
                            hue_count += 1
                    elif key in sat_names:
                        for kommando in kommandos:
                            t = threading.Thread(target=send_cmd_satellite, args=[key,kommando])
                            t.start()                          
                    elif key == "TV":
                        for idx, kommando in enumerate(kommandos):
                            folgen = Timer((float(idx)/5), tv_set_szene, [kommando])
                            folgen.start()                        
                    elif key == "Amp":
                        for kommando in kommandos:
                            marantz_set_szene(kommando) 
                    elif key in TF_LEDs:                
                        for kommando in kommandos:
                            #t = threading.Thread(target=set_TF_LEDs, args=[key, kommando])
                            #t.start()                    
                            set_TF_LEDs(key, kommando)                         
                    elif key == "TuerSPi":
                        for kommando in kommandos:
                            t = threading.Thread(target=TuerSPi, args=[kommando])
                            t.start()
                    elif key == "Interner_Befehl":
                        time.sleep(1)
                        for kommando in kommandos:
                            t = threading.Thread(target=interner_befehl, args=[kommando])
                            t.start() 
                if key in setting:
                    for kommando in kommandos:
                        aes.new_event(description=key + ": " + str(kommando), prio=0)
                        setting_s(key, str(kommando))
                elif key == "Zusatz_Status":
                    time.sleep(1)
                    for kommando in kommandos:
                        #aes.new_event(description=key + ": " + str(kommando) + ": " + str(kommandos.get(kommando)), prio=0)
                        setting_s(str(kommando), str(kommandos.get(kommando)))                             
        if ((szene.get("Szene_folgt") <> "") and (str(szene.get("Szene_folgt")) <> "None")):
            try:
                if type(eval(szene.get("Szene_folgt"))) == list:
                    kommandos = eval(szene.get("Szene_folgt"))
                else:
                    kommandos = [szene.get("Szene_folgt")]
            except NameError as serr:
                kommandos = [szene.get("Szene_folgt")]
            try:
                if type(eval(szene.get("folgt_nach"))) == list:
                    delays = eval(szene.get("folgt_nach"))
                else:
                    delays = [szene.get("folgt_nach")]
            except NameError as serr:
                delays = [szene.get("folgt_nach")]       
            for index, kommando in enumerate(kommandos):
                if "Schlummern" in name:
                    schlummern = Timer(float(delays[index]), set_szene, [str(kommando)])
                    schlummern.start()   
                elif "Bad_ir" in name:
                    bad_ir = Timer(float(delays[index]), set_szene, [str(kommando)])
                    bad_ir.start()                      
                else:
                    folgen = Timer(float(delays[index]), set_szene, [str(kommando)])
                    folgen.start()
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE Szenen SET LastUsed = CURRENT_TIMESTAMP WHERE Name = "'+ name + '"' 
            cur.execute(sql)
        con.close() 

def interner_befehl(befehl):
    if befehl == "deactivate_usb_keys":
        anw_status.deactivate_keys()
    if befehl == "activate_usb_keys":
        anw_status.activate_keys() 
    if befehl == "restart_homecontrol":
        zeit =  time.time()
        now = (strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))  
        setting_s("Laststart", str(now))        
        exectext = "sudo /home/chris/homecontrol/restart_services.sh"
        os.system(exectext)
    if befehl == "keys_in_hub":
        anw_status.keys_in_hub()
    if befehl == "firew_TV_close":
        router.close_fw("192.168.192.26")
        router.close_fw("192.168.192.29")
    if befehl == "firew_TV_open":
        router.open_fw("192.168.192.26")
        router.open_fw("192.168.192.29") 
    if befehl == "update_filme":
        pass
        #plex.
    if befehl == "send_wc_pix":        
        send_wc_pix()
    if befehl == "poweroff":       
        exectext = "sudo poweroff"
        os.system(exectext)          
                    
def marantz_set_szene(szene):
    j = 0
    MarantzSocket.sendto("Update",(MARANTZ_IP,MARANTZ_PORT))
    if str(szene) == "Reset":
        MarantzSocket.sendto("STOP",(MARANTZ_IP,MARANTZ_PORT))
        return
    elif str(szene) == "Save":
        MarantzSocket.sendto("Save",(MARANTZ_IP,MARANTZ_PORT))
        return
    elif str(szene) == "lauter":
        #MarantzSocket.sendto("Save",(MARANTZ_IP,MARANTZ_PORT))
        #szene = "Aktuell"
        #time.sleep(0)
        #m_szene = mdb_marantz_r(str(szene))
        #vol = str(m_szene.get("Volume"))
        #vol = float(vol[1:len(vol)])
        dicti = {}
        dicti["Command"] = "VOL"
        #vol = "0" + str(vol+5)[0:(len(str(vol+5))-2)]
        dicti["Value"] = '3'#vol
        MarantzSocket.sendto(str(dicti),(MARANTZ_IP,MARANTZ_PORT))
        return
    elif str(szene) == "leiser":
        #MarantzSocket.sendto("Save",(MARANTZ_IP,MARANTZ_PORT))
        #szene = "Aktuell"  
        #time.sleep(0)
        #m_szene = mdb_marantz_r(str(szene))
        #vol = str(m_szene.get("Volume"))
        #vol = float(vol[1:len(vol)])
        dicti = {}
        dicti["Command"] = "VOL"
        #vol = "0" + str(vol-5)[0:(len(str(vol-5))-2)]
        dicti["Value"] = '4'#vol
        MarantzSocket.sendto(str(dicti),(MARANTZ_IP,MARANTZ_PORT))
        return
    elif str(szene) == "Update":
        MarantzSocket.sendto("Update",(MARANTZ_IP,MARANTZ_PORT))
        return    
    while mdb_marantz_r('Aktuell').get('Power') == "False" and str(szene) <> "Aus" and j<6:
        ezcontrol.SetSwitch("Video_Audio", "100.0")
        MarantzSocket.sendto("Update",(MARANTZ_IP,MARANTZ_PORT))
        time.sleep(5)
        MarantzSocket.sendto("AMPein",(MARANTZ_IP,MARANTZ_PORT))
        time.sleep(10)
        MarantzSocket.sendto("STOP",(MARANTZ_IP,MARANTZ_PORT))
        time.sleep(15)
        j = j + 1
    if j > 5:
        aes.new_event(description="Probleme mit Marantzcontrol", prio=1)
    if str(szene) == "AMPein":
        MarantzSocket.sendto("AMPein",(MARANTZ_IP,MARANTZ_PORT))         
        return
    m_szene = mdb_marantz_r(str(szene))
    commands = ["Power", "Volume", "Source", "Mute", "Display"]
    shorts = {"Volume":"VOL", "Power":"PWR", "Source":"SRC", "Mute":"AMT", "Display":"DIP"}
    for command in m_szene:
        if ((command in commands) and (str(m_szene.get(command)) <> "None")):
            dicti = {}
            dicti["Command"] = str(shorts.get(command))
            dicti["Value"] = str(m_szene.get(command))
            if str(command) == "Power" and str(m_szene.get(command)) == "True":
                dicti["Value"] = "2"
            if str(command) == "Power" and str(m_szene.get(command)) == "False":
                dicti["Value"] = "1" 
            MarantzSocket.sendto(str(dicti),(MARANTZ_IP,MARANTZ_PORT))
            time.sleep(1)
    if str(m_szene.get("Power")) == "True":
        time.sleep(2)
        MarantzSocket.sendto("STOP",(MARANTZ_IP,MARANTZ_PORT))

def set_TF_LEDs(device, kommando):
    if kommando in ["man", "auto"]:
        mysql_con.set_automode(device=device, mode=kommando)
        return
    Ubersetzung = mdb_sideb_r(kommando)
    if device <>  "Sideb_oben":
        if device == "Sideb_links":
            Ubersetzung['start'] = '[30]'
        if device == "Sideb_mitte":
            Ubersetzung['start'] = '[15]'
        if device == "Sideb_rechts":
            Ubersetzung['start'] = '[0]'            
    if kommando == "toggle":
        time.sleep(1)
        if ezcontrol.GetSwitch("Wohnzimmer_Decke") == "100.0":
            MarantzSocket.sendto("hell",(MARANTZ_IP,MARANTZ_PORT))
            ezcontrol.SetSwitch("Sideboard", "100.0")
        else:
            if str(setting_r("Beleuchtung")) == "Abends":
                folgen = Timer(0.1, set_szene, ['SidebAbends'])
                folgen.start()            
                #set_szene("gemuetlich")
                #MarantzSocket.sendto(str(Ubersetzung),(MARANTZ_IP,MARANTZ_PORT))
                #ezcontrol.SetSwitch("Sideboard", "0.0")
            else:
                MarantzSocket.sendto("aus",(MARANTZ_IP,MARANTZ_PORT))
                ezcontrol.SetSwitch("Sideboard", "0.0")
    else:
        if str(Ubersetzung) <> 'None':
          MarantzSocket.sendto(str(Ubersetzung),(MARANTZ_IP,MARANTZ_PORT))
        else:  
          MarantzSocket.sendto(kommando,(MARANTZ_IP,MARANTZ_PORT))
        
def marantz_fb():
    marantz_set_szene("Update")
    i = 0
    if (str(setting_r("Kommando")) == "Aus"):
        while ((mdb_marantz_r('Aktuell').get('Power') <> mdb_marantz_r(str(setting_r("Kommando"))).get('Power'))):
            marantz_set_szene(str(setting_r("Kommando")))
            marantz_set_szene("Update")
            time.sleep(1)
            i = i + 1
        setting_s("AV_mode", str(setting_r("Kommando")))
        time.sleep(6)
        setting_s("AV_cmd", "0") 
    else:
        while ((mdb_marantz_r('Aktuell').get('Source') <> mdb_marantz_r(str(setting_r("Kommando"))).get('Source'))):
            marantz_set_szene(str(setting_r("Kommando")))
            marantz_set_szene("Update")
            time.sleep(1)
            i = i + 1               
        setting_s("AV_mode", str(setting_r("Kommando")))
        time.sleep(6)
        setting_s("AV_cmd", "0")
    if i > 5:
        aes.new_event(description="Probleme mit Marantzcontrol", prio=0)
                
def tv_set_szene(szene):
    #ineffektiv try with sendkey
    t = threading.Thread(target=tv_remote_lan.sendKey, args=[str(szene)])
    t.start()  
    t = threading.Thread(target=tv_remote.sendKey, args=[str(szene)])
    t.start()  
    if tv_remote_lan.sendKey([str(szene)]) or tv_remote.sendKey([str(szene)]):
        pass
    else:
        count = 0
        while szene <> "KEY_POWEROFF" and not(ping('192.168.192.26')) and not(ping('192.168.192.29')) and count < 10:
            MarantzSocket.sendto("TV_ein",(MARANTZ_IP,MARANTZ_PORT))
            count = count + 1
            time.sleep(10)
        if (szene == "TV_ein"):
            MarantzSocket.sendto("TV_ein",(MARANTZ_IP,MARANTZ_PORT))
        else:
            tv_remote.sendKey([str(szene)])
            tv_remote_lan.sendKey([str(szene)])

def test(bri):
    try:
        int(bri)
    except ValueError:
        auto_l_settings = hue_autolicht(bri)
        print autolicht(helligkeit = 10, offset = auto_l_settings.get("offset"), gradient = auto_l_settings.get("gradient"), mindest=0)                         
            
schlummern = Timer(1, set_szene, ["NONE"])
bad_ir = Timer(1, set_szene, ["NONE"])
            
if __name__ == '__main__':
    main()
