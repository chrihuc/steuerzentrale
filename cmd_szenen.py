# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:21:24 2016

@author: christoph
"""

#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table, setting_s, mdb_read_table_entry, settings_r, mdb_set_table

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV
from cmd_satellites import satelliten
from cmd_internal import internal
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
interna = internal()
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
#    constants.redundancy_.master = True
    print scenes.list_commands()
#    print scenes.execute("Test")
#    time.sleep(10)
#    print scenes.execute("WohnziAnw")
#    
    
class szenen:    
    
    def __init__ (self):
        self.sz_t = szenen_timer(def_to_run = self.execute)
        self.kommando_dict = {}
        self.timeout = datetime.timedelta(hours=0, minutes=0, seconds=15)
        pass
    
    def list_commands(self,gruppe='default'):    
        table = mdb_get_table(constants.sql_tables.szenen.name)
        liste = {'':''}
        if gruppe == "default":
            for szene in table:
                if szene.get("Gruppe") <>"Intern":
                    if str(szene.get("Beschreibung")) <> "None":
                        liste[szene.get("Name")] = szene.get("Beschreibung")
                    else:
                        liste[szene.get("Name")] = szene.get("Name")
        elif gruppe == "alle" or gruppe == "":
            for szene in table:
                if int(szene.get("Id")) > 19:
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
        return (liste)
        

    def __bedingung__(self,bedingungen, verbose = False):
        erfuellt = True
        settings = settings_r() 
        if type(bedingungen) == dict:
#==============================================================================
#             Deprecated
#==============================================================================
            for bedingung in bedingungen:
                if settings.get(bedingung) == None:
                    setting_s(bedingung, '')
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
        elif type(bedingungen) == list:
#==============================================================================
#             new way
#==============================================================================
        #[('Temperatur_Rose','>',['sett','Temperatur_Balkon'])]
            for bedingung in bedingungen:
                if settings.get(bedingung[0]) == None:
                    setting_s(bedingung, '')                
                item, operand, wert = bedingung
                item = settings.get(item)
                if verbose: print item, operand, wert
                if operand == '=':
                    if not float(item) == float(wert):
                        erfuellt = False 
                elif operand == '==':
                    if not str(item) == str(wert):
                        erfuellt = False                         
                elif operand == '<':
                    if not float(item) < float(wert):
                        erfuellt = False  
                elif operand == '>':
                    if not float(item) > float(wert):
                        erfuellt = False   
                elif operand == '<=':
                    if not float(item) <= float(wert):
                        erfuellt = False   
                elif operand == '>=':
                    if not float(item) >= float(wert):
                        erfuellt = False      
                elif operand == '!':
                    if (item) == (wert):
                        erfuellt = False    
                elif operand == 'in':
                    if not (item) in (wert):
                        erfuellt = False                          
        if verbose: print "Ergebniss: ",erfuellt
        return erfuellt
        
    def __return_enum__(self,eingabe):
        if (type(eingabe) == str):
            try:
                if type(eval(eingabe)) == list or type(eval(eingabe)) == dict or type(eval(eingabe)) == tuple:
                    kommandos = eval(eingabe)
                else:
                    kommandos = [eingabe]
            except (NameError, SyntaxError) as e:
                kommandos = [eingabe]
        elif type((eingabe)) == list or type((eingabe)) == dict or type((eingabe)) == tuple:
            return eingabe
        else:
            kommandos = [eingabe]    
        return kommandos 

    def __sub_cmds__(self, szn_id, device, commando, text):
        global kommando_dict
        executed = False
        if szn_id != None:
            t_list = self.kommando_dict.get(szn_id)   
        else:
            t_list = {}
        if device in xs1_devs:
            executed = xs1.set_device(device, commando)
        elif device == "setTask":
            if commando[0] == 'Alle':
                executed = mes.send_direkt(to=mes.alle, titel="Setting", text=str(commando[1]))
            elif commando[0] == 'Zuhause':
                executed = mes.send_zuhause(to=mes.alle, titel="Setting", text=str(commando[1]))  
            else:
                executed = mes.send_zuhause(to=str(commando[0]), titel="Setting", text=str(commando[1]))                 
        elif device in sns_devs:
            executed = sn.set_device(device, commando, text)               
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
#            print device, commando
            executed = sat.set_device(device, commando)                   
        elif device in tvs_devs:
            executed = tv.set_device(device, commando)                                                          
#                        elif key == "Interner_Befehl":
#                            for kommando in kommandos:
#                                t = threading.Thread(target=interner_befehl, args=[commando])
#                                t.start() 
        else:
            executed = True
        if szn_id == None:
            return
        if executed:
            for itm in t_list:
                if itm[0] == device and itm[1] == commando:
                    t_list.remove(itm)
        else:
            aes.new_event(description="Failed: " + str(device) + str(commando), prio=1, karenz = 0.03)
        self.kommando_dict[szn_id] = t_list

    def threadSetDevice(self, device, commando):
        szn_id = None
        text = ''
        t = threading.Thread(target=self.__sub_cmds__, args=[szn_id, device, commando, text])
        t.start()
        
    def threadExecute(self, szene, check_bedingung=False, wert = 0):
        t = threading.Thread(target=self.execute, args=[szene, check_bedingung, wert])
        t.start()         

    def execute(self, szene, check_bedingung=False, wert = 0):
        szene_dict = mdb_read_table_entry(constants.sql_tables.szenen.name, szene)
        start_t = datetime.datetime.now()
#        print start_t, szene_dict.get("Beschreibung"), szene_dict.get("Follows")
        #check bedingung
        bedingungen = {}
        global kommando_dict
        erfuellt = True
        erfolg = False
        szn_id = uuid.uuid4()
        self.kommando_dict[szn_id] = []
        if str(szene_dict.get("Bedingung")) <> "None":
            bedingungen = eval(str(szene_dict.get("Bedingung")))   
        erfuellt = self.__bedingung__(bedingungen)
        if str(szene_dict.get("Latching")) <> 'None':
            next_start = szene_dict.get("LastUsed") + datetime.timedelta(hours=0, minutes=0, seconds=float(szene_dict.get("Latching")))
            if start_t < next_start:
                erfuellt = False
        if str(szene_dict.get("Karenz")) <> 'None':
            Karenz = (szene_dict.get("Karenz"))
        else:
            Karenz = 0.03  
        Prio = (szene_dict.get("Prio"))            
        if check_bedingung:
            return erfuellt
#==============================================================================
# commandos to devices and internal commands        
#==============================================================================
        if erfuellt:
            if (str(szene_dict.get("Delay")) <> "None"):
                time.sleep(float(szene_dict.get("Delay")))
            if str(szene_dict.get("Beschreibung")) in ['None','']:
                aes.new_event(description="Szenen: " + szene, prio=Prio, karenz = Karenz)
            else:
                aes.new_event(description= str(szene_dict.get("Beschreibung")), prio=Prio, karenz = Karenz) 
            interlocks = {}  
            hue_count = 0
            hue_delay = 0            
            if str(szene_dict.get("AutoMode")) == "True":
                interlocks = mdb_read_table_entry(constants.sql_tables.szenen.name,"Auto_Mode")
            for idk, key in enumerate(szene_dict):        
                if ((szene_dict.get(key) <> "") and (str(szene_dict.get(key)) <> "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                    kommandos = self.__return_enum__(szene_dict.get(key))
                    if constants.redundancy_.master:
                        delay = 0
                        for kommando in kommandos:
                            if key in cmd_devs:
                                t_list = self.kommando_dict.get(szn_id)
                                t_list.append([key,kommando])
                                self.kommando_dict[szn_id] = t_list
                            text=szene_dict.get("Durchsage")
                            if kommando == 'warte_1':
                                delay += 1
                            elif kommando == 'warte_3':
                                delay += 3  
                            elif kommando == 'warte_5':
                                delay += 5
                            else:                                
                                t = Timer(delay, self.__sub_cmds__, args=[szn_id, key, kommando, text])
                                t.start()  
#==============================================================================
# Internal                               
#==============================================================================
            key = "intCmd"
            if ((szene_dict.get(key) <> "") and (str(szene_dict.get(key)) <> "None") ):#and (str(interlocks.get(key)) in ["None", "auto"])):
                kommandos = self.__return_enum__(szene_dict.get(key))
                for kommando in kommandos:
                    #print kommando, kommandos.get(kommando)
                    set_del = Timer(0, interna.execute, [kommando])
                    #timer set to 0 for following actions
                    set_del.start()                              
#==============================================================================
# change settings table                                
#==============================================================================
            key = "Setting"
            if ((szene_dict.get(key) <> "") and (str(szene_dict.get(key)) <> "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                kommandos = self.__return_enum__(szene_dict.get(key))
                for kommando in kommandos:
#                    #print kommando, kommandos.get(kommando)
#                    set_del = Timer(0, setting_s, [str(kommando), str(kommandos.get(kommando))])
#                    #timer set to 0 for following actions
#                    set_del.start() 
                    # solution above could give timing issues
                    setting_s(str(kommando), str(kommandos.get(kommando)))
            mdb_set_table(table=constants.sql_tables.szenen.name, device=szene, commands={'LastUsed':start_t})
        elif False:
            if str(szene_dict.get("Beschreibung")) in ['None','']:
                aes.new_event(description="Szene nicht erfuellt: " + szene, prio=1, karenz = Karenz)
            else:
                aes.new_event(description="Szene nicht erfuellt: " + str(szene_dict.get("Beschreibung")), prio=1, karenz = Karenz)                 
#==============================================================================
# cacnel timers                              
#==============================================================================     
        if ((szene_dict.get("Cancels") <> "") and (str(szene_dict.get("Cancels")) <> "None")):
            kommandos = self.__return_enum__(szene_dict.get("Cancels"))   
            for kommando in kommandos:           
                self.sz_t.cancel_timer(parent = szene, child = kommando)
#==============================================================================
# start timer with following actions                               
#==============================================================================
        if ((szene_dict.get("Follows") <> "") and (str(szene_dict.get("Follows")) <> "None")):
            kommandos = self.__return_enum__(szene_dict.get("Follows"))
            for kommando in kommandos:
                szn = kommando[0]
                dlay = kommando[1]
                ex_re = kommando[2]
                immer = False
                depErfolg = 0
                if len(kommando) > 3:
                    immer = not kommando[3]
                if len(kommando) == 5:
                    depErfolg = kommando[4]
                if (immer or erfuellt) and depErfolg == 0:
                    if ex_re == 0:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = False, retrig = True)
                    elif ex_re == 1:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = True, retrig = True)
                    elif ex_re == 2:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = False, retrig = False)  
#==============================================================================
# Check for timeout
#==============================================================================
        while datetime.datetime.now() - start_t < self.timeout:
            t_list = self.kommando_dict.get(szn_id)
            time.sleep(.1)
            if len(t_list) == 0:
                erfolg = True
                # write back to table
                break
        t_list = self.kommando_dict.get(szn_id)
        for item in t_list:
            aes.new_event(description="CMD Timeout: " + str(item), prio=1, karenz = 0.03)
        del self.kommando_dict[szn_id]
#==============================================================================
# start timer with following actions nur wenn erfolg oder nicht erfolg                              
#==============================================================================
        if ((szene_dict.get("Follows") <> "") and (str(szene_dict.get("Follows")) <> "None")):
            kommandos = self.__return_enum__(szene_dict.get("Follows"))
            for kommando in kommandos:
                szn = kommando[0]
                dlay = kommando[1]
                ex_re = kommando[2]
                immer = False
                depErfolg = 0
                if len(kommando) > 3:
                    immer = kommando[3]
                if len(kommando) == 5:
                    depErfolg = kommando[4]
                if (immer or erfuellt) and ((depErfolg == 1 and erfolg) or (depErfolg == 2 and not erfolg)):
                    if ex_re == 0:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = False, retrig = True)
                    elif ex_re == 1:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = True, retrig = True)
                    elif ex_re == 2:
                        self.sz_t.retrigger_add(parent = szene,delay = float(dlay), child = szn, exact = False, retrig = False)           
        return erfolg

if __name__ == '__main__':
    main()      