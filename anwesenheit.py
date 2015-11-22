#!/usr/bin/env python

import constants

from classes import ping
import MySQLdb as mdb
import requests
from requests import ConnectionError
from mysql_con import setting_s, setting_r
from alarmevents import alarm_event

#Ping Handys alle 2 min countdown von 5 wenn nicht Ping false (aendern nach 10 min)
#Check USB-Schluesselanhaenger alle 30 min aendere status nach 1 std
#Besucher
#Besondere Schluessel
#
#Bewohner Table: Name, Handy_IP, USB_ID, Handy_State, USB_State
#Besucher Table: Name, USB_ID, USB_State
#
#verschiedene states: Urlaub -1, Keiner_da 0, Einer_da 1, Alle_da 2, Nur_Besuch 0.5

#wert wenn ping erfoglreich
ping_max = 5
ping_weg = 0
ping_urlaub = -3120
usb_max = 15
usb_anw = 1
usb_weg = 0
usb_min = -10
usb_deact = -15
#sicherheitsfaktor gegen zurueckgelassenen schluessel 5 = 10 min
sf_usb = 5

aes = alarm_event()

def main():
    status = anwesenheit()
    print status.check_all()

class anwesenheit:
    def __init__(self):
        self.data = []

    def read_mysql(self, table):
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

    def write_mysql(self, table, name, setting, wert):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE '+ table +' SET ' + str(setting) + ' = "' + str(wert) + '" WHERE Name = "'+ str(name) + '"'
            cur.execute(sql)
        con.close()         
        
    def check_handy (self, ip, wert):   
        if ping(ip):
            return ping_max
        else:
            wert -= 1
        if wert <= ping_urlaub:
            wert = ping_urlaub
        return wert
     
    def check_all(self):
        Bewohner = self.read_mysql("Bewohner")
        Besucher = self.read_mysql("Besucher")
        Anwesenheit = 0
        Besuch = 0
        Urlaub = True
        Einbruch = True
        dicti = {}
        for name in Bewohner:
            ping_wert_o = name.get("Handy_State")
            ping_wert = self.check_handy(name.get("Handy_IP"), ping_wert_o)
            self.write_mysql(table="Bewohner",name=name.get("Name"),setting="Handy_State",wert=ping_wert)
            usb_wert = name.get("USB_State")
            if (ping_wert > ping_weg or usb_wert >usb_weg): #ansonsten alles aus sobald der schluessel gezogen wird and not(usb_wert < usb_wert_o):
                Anwesenheit += 1
                if str(setting_r(name.get("Name")+"_anwesend")) == "0":
                    aes.new_event(description=name.get("Name")+" heimgekommen", prio=0)
                setting_s(name.get("Name")+"_anwesend","1")
            else:
                if str(setting_r(name.get("Name")+"_anwesend")) == "1":
                    aes.new_event(description=name.get("Name")+" weggegangen", prio=0)                    
                setting_s(name.get("Name")+"_anwesend","0")
            if ping_wert > ping_urlaub or usb_wert > usb_min:    
                Urlaub = False
            if (ping_wert_o < ping_wert):
                Einbruch = False 
        for name in Bewohner:
            usb_wert = name.get("USB_State")
            if (usb_wert >usb_weg):
                Anwesenheit += 1
        if Urlaub:
            Anwesenheit = -1
        if str(setting_r("Einbruch")) == "True" and not Einbruch:
            setting_s("Einbruch","False")
        dicti['Anwesenheit'] = Anwesenheit
        setting_s("Anwesenheit", Anwesenheit)
        dicti['Besuch'] = Besuch
        dicti['Einbruch'] = Einbruch
        return dicti

    def deactivate_keys(self):
        Bewohner = self.read_mysql("Bewohner")
        for name in Bewohner:
            usb_wert = name.get("USB_State")
            if usb_wert > usb_weg:
                self.write_mysql(table="Bewohner",name=name.get("Name"),setting="USB_State",wert=usb_deact)

    def activate_keys(self):
        Bewohner = self.read_mysql("Bewohner")
        for name in Bewohner:
            usb_wert = name.get("USB_State")
            if usb_wert == usb_deact:
                self.write_mysql(table="Bewohner",name=name.get("Name"),setting="USB_State",wert=usb_anw)                    

    def keys_in_hub(self):
        Bewohner = self.read_mysql("Bewohner")                      
        for name in Bewohner:
            if name.get("Handy_State") > 3 and name.get("USB_State") <= 0:
                aes.new_event(description=name.get("Name")+" bitte Schluessel einstecken.", prio=2)
           
if __name__ == '__main__':
    main()