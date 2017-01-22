# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:58:42 2016

@author: chuckle
"""

import constants
import git
from alarmevents import alarm_event

aes = alarm_event()

def ping(IP, number = 1):
    pinged = False
    if IP == None:
        return False
    else:
        lifeline = re.compile(r"(\d) received")
        report = ("No response","Partial Response","Alive")
        for i in range(0,number):
            pingaling = os.popen("ping -q -c 2 "+IP,"r")
            sys.stdout.flush()
            while 1==1:
               line = pingaling.readline()
               if not line: break
               igot = re.findall(lifeline,line)
               if igot:
                if int(igot[0])==2:
                    pinged = True
                else:
                    pass
        return pinged

class internal:
    
    def __init__ (self):
        pass

    def list_commands(self):
        return ['Update']
        
    def execute(self, commd):
        if commd == 'Update':
            self.git_update()
        
    def git_update(self):
        g = git.cmd.Git()
        g.pull()
        g.reset('--hard')
        print "Update done, exiting"
        aes.new_event(description="Update performed, restarting", prio=1)
        constants.run = False


class anwesenheit:
    def __init__(self):
        self.data = []

    def check_handy(self, ip, wert):
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
            self.write_mysql(table="Bewohner", name=name.get("Name"), setting="Handy_State", wert=ping_wert)
            usb_wert = name.get("USB_State")
            if (
                    ping_wert > ping_weg or usb_wert > usb_weg):  # ansonsten alles aus sobald der schluessel gezogen wird and not(usb_wert < usb_wert_o):
                Anwesenheit += 1
                if str(setting_r(name.get("Name") + "_anwesend")) == "0":
                    aes.new_event(description=name.get("Name") + " heimgekommen", prio=0)
                setting_s(name.get("Name") + "_anwesend", "1")
            else:
                if str(setting_r(name.get("Name") + "_anwesend")) == "1":
                    aes.new_event(description=name.get("Name") + " weggegangen", prio=0)
                setting_s(name.get("Name") + "_anwesend", "0")
            if ping_wert > ping_urlaub or usb_wert > usb_min:
                Urlaub = False
            if (ping_wert_o < ping_wert):
                Einbruch = False
        for name in Bewohner:
            usb_wert = name.get("USB_State")
            if (usb_wert > usb_weg):
                Anwesenheit += 1
        if Urlaub:
            Anwesenheit = -1
        if str(setting_r("Einbruch")) == "True" and not Einbruch:
            setting_s("Einbruch", "False")
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
                self.write_mysql(table="Bewohner", name=name.get("Name"), setting="USB_State", wert=usb_deact)

    def activate_keys(self):
        Bewohner = self.read_mysql("Bewohner")
        for name in Bewohner:
            usb_wert = name.get("USB_State")
            if usb_wert == usb_deact:
                self.write_mysql(table="Bewohner", name=name.get("Name"), setting="USB_State", wert=usb_anw)

    def keys_in_hub(self):
        Bewohner = self.read_mysql("Bewohner")
        for name in Bewohner:
            if name.get("Handy_State") > 3 and name.get("USB_State") <= 0:
                aes.new_event(description=name.get("Name") + " bitte Schluessel einstecken.", prio=2)
