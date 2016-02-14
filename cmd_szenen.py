# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:21:24 2016

@author: christoph
"""

#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table, setting_s, mdb_read_table_entry, settings_r

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV
from cmd_satellites import satelliten
from alarmevents import alarm_event
from szn_timer import szenen_timer
from messaging import messaging

import threading
from threading import Timer
import uuid
import datetime
import time

xs1 = myezcontrol(constants.xs1_.IP)
hue = hue_lights()
sn = sonos()
tv = TV()
sat = satelliten()
xs1_devs = xs1.list_devices()
hue_devs = hue.list_devices()
sns_devs = sn.list_devices()
tvs_devs = tv.list_devices()
sat_devs = sat.list_devices()
cmd_devs = xs1_devs + hue_devs + sns_devs + tvs_devs + sat_devs
aes = alarm_event()
mes = messaging()


def main():
    scenes = szenen()
    constants.redundancy_.master = True
    print scenes.list_commands()
    scenes.execute("Test")
    
class szenen:    
    
    def __init__ (self):
        self.sz_t = szenen_timer(def_to_run = self.execute)
        self.kommando_dict = {}
        self.timeout = datetime.timedelta(hours=0, minutes=0, seconds=10)
        pass
    
    def list_commands(self,gruppe='default'):    
        table = mdb_get_table(constants.sql_tables.szenen.name)
        liste = {}
        if gruppe == "default":
            for szene in table:
                if szene.get("Gruppe") <>"Intern":
                    if str(szene.get("Beschreibung")) <> "None":
                        liste[szene.get("Name")] = szene.get("Beschreibung")
                    else:
                        liste[szene.get("Name")] = szene.get("Name")
        elif gruppe == "alle":
            for szene in table:
                if str(szene.get("Beschreibung")) <> "None":
                    liste[szene.get("Name")] = szene.get("Beschreibung")
                else:
                    liste[szene.get("Name")] = szene.get("Name")                        
        else:
            for szene in table:
                if szene.get("Gruppe") == gruppe:
                    if str(szene.get("Beschreibung")) <> "None":
                        liste[szene.get("Name")] = szene.get("Beschreibung")
                    else:
                        liste[szene.get("Name")] = szene.get("Name")           
        return liste

    def __bedingung__(self,bedingungen):
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
            except Exception:
                if not(str(settings.get(bedingung)) in bedingungen.get(bedingung)):
                    erfuellt = False      
        return erfuellt

    def __sub_cmds__(self, szn_id, device, commando):
        global kommando_dict
        executed = False
        t_list = self.kommando_dict.get(szn_id)      
        if device in xs1_devs:
            executed = xs1.set_device(device, commando)
        elif device == "set_Task":
            executed = mes.send_direkt(to=mes.alle, titel="Setting", text=str(commando)) 
        elif device == "set_Task_zuhause":
            executed = mes.send_zuhause(to=mes.alle, titel="Setting", text=str(commando))                  
        elif device in sns_devs:
            executed = sn.set_device(device, commando)               
        elif device in hue_devs:
            executed = hue.set_device(device, commando)  
#            for kommando in kommandos:
#                if hue_count > 1:
#                    hue_delay += 0.75
#                    hue_count = 0
#                hue_del = Timer(hue_delay, hue.set_device, [key, commando])
#                hue_del.start()
#                hue_count += 1
        elif device in sat_devs:
            executed = sat.set_device(device, commando)                            
        elif device == tvs_devs:
            executed = tv.set_device(device, commando)         
#            for idx, kommando in enumerate(kommandos):
#                folgen = Timer((float(idx)/5), tv.set_device, [key,commando])
#                folgen.start()                                                 
#                        elif key == "Interner_Befehl":
#                            for kommando in kommandos:
#                                t = threading.Thread(target=interner_befehl, args=[commando])
#                                t.start()    
        if executed:
            for itm in t_list:
                if itm[0] == device and itm[1] == commando:
                    t_list.remove(itm)
        self.kommando_dict[szn_id] = t_list

    def execute(self, szene):
        szene_dict = mdb_read_table_entry(constants.sql_tables.szenen.name, szene)
        start_t = datetime.datetime.now()
        #check bedingung
        bedingungen = {}
        global kommando_dict
        erfuellt = True
        erfolg = False
        szn_id = uuid.uuid4()
        self.kommando_dict[szn_id] = []
        if str(szene_dict.get("Bedingung")) <> "None":
            bedingungen = eval(szene_dict.get("Bedingung"))    
        erfuellt = self.__bedingung__(bedingungen)
#==============================================================================
# commandos to devices and internal commands        
#==============================================================================
        if erfuellt:
            if str(szene_dict.get("Beschreibung")) in ['None','']:
                aes.new_event(description="Szenen: " + szene, prio=(szene_dict.get("Prio")), karenz = 0.03)
            else:
                aes.new_event(description= str(szene_dict.get("Beschreibung")), prio=(szene_dict.get("Prio")), karenz = 0.03) 
            interlocks = {}  
            hue_count = 0
            hue_delay = 0            
            if str(szene_dict.get("AutoMode")) == "True":
                interlocks = mdb_read_table_entry(constants.sql_tables.szenen.name,"Auto_Mode")
            for idk, key in enumerate(szene_dict):        
                if ((szene_dict.get(key) <> "") and (str(szene_dict.get(key)) <> "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                    if (type(szene_dict.get(key)) == str):
                        try:
                            if type(eval(szene_dict.get(key))) == list or type(eval(szene_dict.get(key))) == dict:
                                kommandos = eval(szene_dict.get(key))
                            else:
                                kommandos = [szene_dict.get(key)]
                        except:
                            kommandos = [szene_dict.get(key)]
                    else:
                        kommandos = [szene_dict.get(key)]
                    if constants.redundancy_.master:
                        for kommando in kommandos:
                            if key in cmd_devs:
                                t_list = self.kommando_dict.get(szn_id)
                                t_list.append([key,kommando])
                                self.kommando_dict[szn_id] = t_list
                            t = threading.Thread(target=self.__sub_cmds__, args=[szn_id, key, kommando])
                            t.start()                         
#==============================================================================
# change settings table                                
#==============================================================================
        key = "Setting"
        if ((szene_dict.get(key) <> "") and (str(szene_dict.get(key)) <> "None") and (str(interlocks.get(key)) in ["None", "auto"])):
            if (type(szene_dict.get(key)) == str):
                try:
                    if type(eval(szene_dict.get(key))) == list or type(eval(szene_dict.get(key))) == dict:
                        kommandos = eval(szene_dict.get(key))
                    else:
                        kommandos = [szene_dict.get(key)]
                except NameError:
                    kommandos = [szene_dict.get(key)]
            else:
                kommandos = [szene_dict.get(key)]  
            for kommando in kommandos:
                set_del = Timer(1, setting_s, [str(kommando), str(kommandos.get(kommando))])
                set_del.start()  
#==============================================================================
# start timer with following actions                               
#==============================================================================
        if ((szene_dict.get("Follows") <> "") and (str(szene_dict.get("Follows")) <> "None")):
            try:
                if type(eval(szene_dict.get("Follows"))) == list:
                    kommandos = eval(szene.get("Follows"))
                else:
                    kommandos = [szene_dict.get("Follows")]
            except NameError:
                kommandos = [szene_dict.get("Follows")]      
            for kommando in kommandos:
                sub_cmds = eval(kommando)
                if sub_cmds[2] == 0:
                    self.sz_t.retrigger_add(parent = szene,delay = sub_cmds[1], child = sub_cmds[0], exact = False, retrig = True)
                elif sub_cmds[2] == 1:
                    self.sz_t.retrigger_add(parent = szene,delay = sub_cmds[1], child = sub_cmds[0], exact = True, retrig = True)
                elif sub_cmds[2] == 2:
                    self.sz_t.retrigger_add(parent = szene,delay = sub_cmds[1], child = sub_cmds[0], exact = False, retrig = False)                    
#==============================================================================
# Check for timeout
#==============================================================================
        while datetime.datetime.now() - start_t < self.timeout:
            t_list = self.kommando_dict.get(szn_id)
            time.sleep(.1)
            if len(t_list) == 0:
                erfolg = True
                break
        t_list = self.kommando_dict.get(szn_id)
        for item in t_list:
            aes.new_event(description="CMD Timeout: " + str(item), prio=0, karenz = 0.03)
        del self.kommando_dict[szn_id]
        return erfolg

if __name__ == '__main__':
    main()      