# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:21:24 2016

@author: christoph
"""

#!/usr/bin/env python

import threading
from threading import Timer
import uuid
import datetime
import time
import psutil

import constants

from alarm_event_messaging import alarmevents
from alarm_event_messaging import messaging

from database import mysql_connector as msqc

from outputs import hue

from outputs import internal
from outputs import samsung
from outputs import satellites
from outputs import sonos
from outputs import xs1

from tools import szn_timer
from tools import toolbox
#toolbox.log('debug on')

try:
    from outputs import tradfri
    trads = tradfri.Tradfri_lights()
    trads_devs = msqc.tables.akt_type_dict['TRADFRI']
except KeyError:
    trads = None
    trads_devs = []

xs1 = xs1.XS1()
hues = hue.Hue_lights()
sn = sonos.Sonos()
tv = samsung.TV()
sat = satellites.Satellite()
interna = internal.Internal()
xs1_devs = msqc.tables.akt_type_dict['XS1']
hue_devs = msqc.tables.akt_type_dict['HUE']
sns_devs = msqc.tables.akt_type_dict['SONOS']
tvs_devs = msqc.tables.akt_type_dict['TV']
sat_devs = msqc.tables.akt_type_dict['SATELLITE']
sat_devs += msqc.tables.akt_type_dict['ZWave']
loc_devs = msqc.tables.akt_type_dict['Local']
cmd_devs = xs1_devs + hue_devs + sns_devs + tvs_devs + sat_devs  + trads_devs
aes = alarmevents.AES()
mes = messaging.Messaging()

# TODO Tests split adress from hks
# Add Aktor_bedingung


class Szenen(object):

    kommando_dict = {}
    timeout = datetime.timedelta(hours=0, minutes=0, seconds=30)
    sz_t = szn_timer.Szenen_Timer()
    running_list = {} # gibt probleme mit changes while iterating, müsste mit locks gearbeitet werden
    high_cpu_cnt = 0
    # liste locken dann ändern

    def __init__ (self):
#        self.sz_t = szn_timer.Szenen_Timer(callback = self.execute)
#        self.kommando_dict = {}
#        self.timeout = datetime.timedelta(hours=0, minutes=0, seconds=15)
        Szenen.sz_t.callback = self.execute
        Szenen.sz_t.load()
        pass

    @classmethod
    def callback_receiver(cls, payload, *args, **kwargs):
        if toolbox.kw_unpack(kwargs,'typ') == 'SetDevice':
            cls.threadSetDevice(payload['Device'], payload['Command'])
        if toolbox.kw_unpack(kwargs,'typ') == 'return':
            if 'szn_id' in payload:
                t_list = cls.kommando_dict.get(payload['szn_id'])
                if toolbox.kw_unpack(kwargs,'value') == True:
                    for itm in t_list:
                        if itm[0] == payload['Device'] and itm[1] == payload['Szene']:
                            t_list.remove(itm)
                cls.kommando_dict[payload['szn_id']] = t_list
        elif ('Name' in payload) and ('Value' in payload) and not toolbox.kw_unpack(kwargs,'typ') == 'output':
            cls.trigger_scenes(payload['Name'], payload['Value'])
        if toolbox.kw_unpack(kwargs,'typ') == 'ExecSzene':
            if toolbox.kw_unpack(payload,'desc'):
                cls.threadExecute(payload['Szene'], desc=payload['desc'])
            else:
                cls.threadExecute(payload['Szene'])

    @classmethod
    def reset_cpu_cnt(cls):
        cls.high_cpu_cnt = 0
        
    @classmethod
    def trigger_scenes(cls, device, value):
        szns, desc, heartbt, payloads = msqc.inputs(device,value)
#        hearbeat supervision
#        if not ((heartbt is None) or (device is None)):
#            cls.timer_add(cls.execute, parent=None, device=desc, delay=float(heartbt), child='Input_sup', exact=True, retrig=True)
#        for szene in szns:
        for i, szene in enumerate(szns):
            if szene != None:
                cls.threadExecute(szene, check_bedingung=False, wert=value, device=desc, payload=payloads[i])

    @staticmethod
    def list_commands(gruppe='default'):
        table = msqc.mdb_get_table(constants.sql_tables.szenen.name)
        liste = {'':''}
        if not isinstance(gruppe, list):
            gruppe = [gruppe]
        for eintrag in gruppe:
            if eintrag == "default":
                for szene in table:
                    if szene.get("Gruppe") !="Intern":
                        if str(szene.get("Beschreibung")) != "None":
                            liste[szene.get("Name")] = szene.get("Beschreibung")
                        else:
                            liste[szene.get("Name")] = szene.get("Name")
            elif eintrag == "alle" or eintrag == "":
                for szene in table:
                    if int(szene.get("Id")) > 19:
                        if str(szene.get("Beschreibung")) != "None":
                            liste[szene.get("Name")] = szene.get("Beschreibung")
                        else:
                            liste[szene.get("Name")] = szene.get("Name")
            else:
                for szene in table:
                    if szene.get("Gruppe") == eintrag:
                        if str(szene.get("Beschreibung")) != "None":
                            liste[szene.get("Name")] = szene.get("Beschreibung")
                        else:
                            liste[szene.get("Name")] = szene.get("Name")
        return (liste)


    @staticmethod
    def __bedingung__(bedingungen, verbose = False):
        erfuellt = True
        settings = msqc.settings_r()
        if type(bedingungen) == dict:
#==============================================================================
#             Deprecated
#==============================================================================
            for bedingung in bedingungen:
                if settings.get(bedingung) == None:
                    msqc.setting_s(bedingung, '')
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
#                for i, wert in enumerate(bedingungen):
#                    for j, eintrag in enumerate(wert):
#                        bedingungen[i][j]=mysql_connector.re_calc(eintrag)
                try:
                    inpt, operand, wert = bedingung
                    wert = msqc.re_calc(wert)
                except:
                    print(bedingung)
                    return False
                if msqc.setting_r(inpt) == None:
                    print(inpt, 'gibts nicht')
#                    msqc.setting_s(inpt, '')
#                item = settings.get(item)
                item = msqc.setting_r(inpt)
                valid = msqc.valid_r(inpt)
                if verbose: print(item, operand, wert)
                if operand == '=':                          # mathematisch gleich
                    if not float(item) == float(wert):
                        erfuellt = False
                elif operand == '==':                       # String gleich
                    if not str(item) == str(wert):
                        erfuellt = False
                elif operand == '<':
                    if not float(item) < float(str(wert)):
                        erfuellt = False
                elif operand == '>':
                    if not float(item) > float(str(wert)):
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
                elif operand == 'valid':
                    if not (str(valid) == wert):
                        erfuellt = False                        
        if verbose: print( "Ergebniss: ",erfuellt)
        return erfuellt

    @staticmethod
    def __return_enum__(eingabe):
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

    @classmethod
    def __sub_cmds__(cls, szn_id, device, commando, text):
        try:
            adress = msqc.get_device_adress(device)
            system = adress.split(".")[0]
        except:
            adress = device
            system = ''
        executed = False
        if szn_id != None:
            t_list = cls.kommando_dict.get(szn_id)
        else:
            t_list = {}
        if commando in ["man", "auto"]:
            msqc.set_val_in_szenen(device=device, szene="Auto_Mode", value=commando)
        elif commando in ["autoToggle"]:
            current = msqc.get_val_in_szenen(device=device, szene="Auto_Mode")
            if 'auto' in current:
                msqc.set_val_in_szenen(device=device, szene="Auto_Mode", value='man')
            else:
                msqc.set_val_in_szenen(device=device, szene="Auto_Mode", value='auto')
        elif True: #szn_id == None or szn_id in cls.running_list:
            if device in xs1_devs:
                executed = xs1.set_device(adress, str(commando))
            elif device == "setTask":
                if commando[0] == 'Alle':
                    executed = mes.send_direkt(to=mes.alle, titel="Setting", text=str(commando[1]))
                elif commando[0] == 'Zuhause':
                    executed = mes.send_zuhause(to=mes.alle, titel="Setting", text=str(commando[1]))
                else:
                    executed = mes.send_zuhause(to=str(commando[0]), titel="Setting", text=str(commando[1]))
            elif device in sns_devs:
                executed = sn.set_device(adress, commando, text)
            elif device in hue_devs:
                executed = hues.set_device(adress, commando)
    #            for kommando in kommandos:
    #                if hue_count > 1:
    #                    hue_delay += 0.75
    #                    hue_count = 0
    #                hue_del = Timer(hue_delay, hue.set_device, [key, commando])
    #                hue_del.start()
    #                hue_count += 1
            elif any([device in dev for dev in trads_devs]):
                executed = trads.set_device(adress, commando)
            elif device in sat_devs:
                executed = sat.set_device(adress, commando)
            elif device in tvs_devs:
                executed = tv.set_device(adress, commando)
    #                        elif key == "Interner_Befehl":
    #                            for kommando in kommandos:
    #                                t = threading.Thread(target=interner_befehl, args=[commando])
    #                                t.start()
            elif device in msqc.tables.akt_type_dict['Local']:
                com_set = msqc.mdb_read_table_entry(db=msqc.tables.akt_cmd_tbl_dict[device], entry=commando)
                payload = {'Device': device, 'Szene': commando, 'Szene_id': szn_id}
                if com_set: payload.update(com_set)
                system = adress.split(".")[0]
                toolbox.communication.send_message(payload, typ='output', receiver=system, adress=adress)
            else:
                executed = True
        else:
            executed = True                
        if executed:
# TODO: Return True and value and write value to table
            if device not in ['Name', 'Id']:
                msqc.set_val_in_szenen(device=device, szene="Value", value=commando)
        if szn_id == None:
            return
        if executed:
            for itm in t_list:
                if itm[0] == device and itm[1] == commando:
                    t_list.remove(itm)
        elif not device in msqc.tables.akt_type_dict['Local']:
            aes.new_event(description="Failed: " + str(device) + str(commando), prio=1, karenz = 0.03)
        cls.kommando_dict[szn_id] = t_list

    @classmethod
    def threadSetDevice(cls, device, commando):
        szn_id = None
        text = ''
        t = threading.Thread(target=cls.__sub_cmds__, args=[szn_id, device, commando, text])
        t.start()

    @classmethod
    def threadExecute(cls, szene, check_bedingung=False, wert=0, device=None, desc='', payload=None):
        t = threading.Thread(target=cls.execute, args=[szene, check_bedingung, wert, device, False, desc, payload])
        t.start()

    @classmethod
    def execute(cls, szene, check_bedingung=False, wert=0, device=None, noDelay=False, desc='', payload=None):
#        ct = datetime.datetime.now()
        toolbox.log(szene)
        if constants.passive:
            return True
        use = psutil.cpu_percent()
        msqc.writeInfluxDb('Vm1ZIM1SER1CP01', use, datetime.datetime.utcnow())
        if use > 99:
#            print("ProcessorLeistung zu hoch")
            cls.high_cpu_cnt += 1
            if cls.high_cpu_cnt > 10:
                aes.new_event(description="ProcessorLeistung zu hoch bei: " + szene, prio=9, karenz = 0.03)
                t = toolbox.OwnTimer(10, function=cls.reset_cpu_cnt, name="resetcpu")
                t.start()            
                return False
        szene_dict = msqc.mdb_read_table_entry(constants.sql_tables.szenen.name, szene)
        start_t = datetime.datetime.now()
        #check bedingung
        bedingungen = {}
        erfuellt = True
        erfolg = False
        szn_id = uuid.uuid4()
        cls.kommando_dict[szn_id] = []
        if str(szene_dict.get("Bedingung")) != "None":
            bedingungen = eval(str(szene_dict.get("Bedingung")))
        # wir warten erstmal den Delay ab, und prüfen dann die Bedingung, das ermöglicht eine Persitenz des Inputs
        # e.g. Temp fällt unter 0 Grad, 30sec später prüfen wir die Bedingung, gilt sie (kein neuer Messwert) führen wir die Szene aus
        if (str(szene_dict.get("Delay")) != "None") and (float(szene_dict.get("Delay")) > 0) and not noDelay:
            cls.timer_add(cls.execute, parent = szene,delay = float(szene_dict.get("Delay")), child = szene, exact = False, retrig = False, noDelay=True)
            return True
#            time.sleep(float(szene_dict.get("Delay")))            
        erfuellt = cls.__bedingung__(bedingungen)
        if str(szene_dict.get("Latching")) != 'None' and str(szene_dict.get("LastUsed")) != 'None':
            next_start = szene_dict.get("LastUsed") + datetime.timedelta(hours=0, minutes=0, seconds=float(szene_dict.get("Latching")))
            if start_t < next_start:
                erfuellt = False
        if str(szene_dict.get("Karenz")) != 'None':
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
            #cls.running_list[szn_id] = szene
            if desc != '':
                text = desc
            elif str(szene_dict.get("Beschreibung")) in ['None','']:
                text = ''
            else:
                if device:
                    text = '%s, %s = %s' % (str(szene_dict.get("Beschreibung")), device, wert)
                else:
                    text = str(szene_dict.get("Beschreibung"))
            aes.new_event(description=text, to=szene_dict.get("MQTTChannel"), prio=Prio, karenz=Karenz, payload=payload)
            interlocks = {}
            if str(szene_dict.get("AutoMode")) == "True":
                interlocks = msqc.mdb_read_table_entry(constants.sql_tables.szenen.name,"Auto_Mode")              
            for idk, key in enumerate(szene_dict):
                if ((szene_dict.get(key) != "") and (str(szene_dict.get(key)) != "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                    kommandos = cls.__return_enum__(szene_dict.get(key))
                    if constants.redundancy_.master:
                        delay = 0
                        for kommando in kommandos:
                            kommando = msqc.re_calc(kommando)
                            if key in cmd_devs:
                                t_list = cls.kommando_dict.get(szn_id)
                                t_list.append([key,kommando])
                                cls.kommando_dict[szn_id] = t_list
                            text=szene_dict.get("Durchsage")
                            if kommando == 'warte_1':
                                delay += 1
                            elif kommando == 'warte_3':
                                delay += 3
                            elif kommando == 'warte_5':
                                delay += 5
                            else:
                                t = Timer(delay, cls.__sub_cmds__, args=[szn_id, key, kommando, text])
                                t.start()
#==============================================================================
# Internal
#==============================================================================                               
            key = "intCmd"
            if ((szene_dict.get(key) != "") and (str(szene_dict.get(key)) != "None") ):#and (str(interlocks.get(key)) in ["None", "auto"])):
                kommandos = cls.__return_enum__(szene_dict.get(key))
                for kommando in kommandos:
                    set_del = Timer(0, interna.execute, [kommando])
                    #timer set to 0 for following actions
                    set_del.start()
#==============================================================================
# change settings table
#==============================================================================
            key = "Setting"
            if ((szene_dict.get(key) != "") and (str(szene_dict.get(key)) != "None") and (str(interlocks.get(key)) in ["None", "auto"])):
                kommandos = cls.__return_enum__(szene_dict.get(key))
                for kommando in kommandos:
#                    set_del = Timer(0, setting_s, [str(kommando), str(kommandos.get(kommando))])
#                    #timer set to 0 for following actions
#                    set_del.start()
                    # solution above could give timing issues
                    value = msqc.re_calc(str(kommandos.get(kommando)))
                    msqc.setting_s(str(kommando), value)
            msqc.mdb_set_table(table=constants.sql_tables.szenen.name, device=szene, commands={'LastUsed':start_t})
        elif False:
            if str(szene_dict.get("Beschreibung")) in ['None','']:
                aes.new_event(description="Szene nicht erfuellt: " + szene, prio=1, karenz = Karenz)
            else:
                aes.new_event(description="Szene nicht erfuellt: " + str(szene_dict.get("Beschreibung")), prio=1, karenz = Karenz)
#==============================================================================
# cacnel timers
#==============================================================================
        if ((szene_dict.get("Cancels") != "") and (str(szene_dict.get("Cancels")) != "None") and erfuellt):
            kommandos = cls.__return_enum__(szene_dict.get("Cancels"))
            for kommando in kommandos:
                cls.sz_t.cancel_timer(parent = szene, child = kommando)
                #cls.running_list = {key:val for key, val in cls.running_list.items() if val != kommando}  # was ist mit der Szenen die ich bin? 
#==============================================================================
# start timer with following actions
# ['Szene', delay(s), exact_retrigger [0 nicht exact & retrig,1,2 nicht nicht], selben bedingungen, abhängig erfolg]                
#==============================================================================
        if ((szene_dict.get("Follows") != "") and (str(szene_dict.get("Follows")) != "None")):
            kommandos = cls.__return_enum__(szene_dict.get("Follows"))
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
#                    if Prio > 0:
#                        print("szene timed start", start_t, szn, dlay)
                    if ex_re == 0:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = False, retrig = True)
                    elif ex_re == 1:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = True, retrig = True)
                    elif ex_re == 2:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = False, retrig = False)
#==============================================================================
# Check for timeout
#==============================================================================
        if erfuellt:
            while datetime.datetime.now() - start_t < cls.timeout:
                t_list = cls.kommando_dict.get(szn_id)
                time.sleep(.1)
                if len(t_list) == 0:
                    erfolg = True
                    # write back to table
                    break
        t_list = cls.kommando_dict.get(szn_id)
        for item in t_list:
            aes.new_event(description="CMD Timeout: " + str(item), prio=1, karenz = 0.03)
        del cls.kommando_dict[szn_id]
#==============================================================================
# start timer with following actions nur wenn erfolg oder nicht erfolg
#==============================================================================
        if ((szene_dict.get("Follows") != "") and (str(szene_dict.get("Follows")) != "None")):
            kommandos = cls.__return_enum__(szene_dict.get("Follows"))
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
#                    if Prio > 0:
#                        print("szene timed start", start_t, szn, dlay)                    
                    if ex_re == 0:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = False, retrig = True)
                    elif ex_re == 1:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = True, retrig = True)
                    elif ex_re == 2:
                        cls.timer_add(cls.execute, parent = szene,delay = float(dlay), child = szn, exact = False, retrig = False)
#        print('Time spend on szene: ', str(datetime.datetime.now() - start_t))
        #cls.running_list.pop(szn_id)
        return erfolg


#    sz_t.callback = execute

    @classmethod
    def timer_add(cls, callback, parent, delay, child, exact, retrig, device=None, noDelay=False):
        cls.sz_t.callback = callback
#        t = Timer(0, cls.sz_t.retrigger_add, args=[parent, delay, child, exact, retrig, device, noDelay])
#        t.start()        
        cls.sz_t.retrigger_add(parent, delay, child, exact, retrig, device, noDelay)

toolbox.communication.register_callback(Szenen.callback_receiver)
