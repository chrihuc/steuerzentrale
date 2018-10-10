#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

#!/usr/bin/env python

import constants

import MySQLdb as mdb
import time

from database import mysql_connector
from alarm_event_messaging import alarmevents

from tools import toolbox

from pytradfri.api.libcoap_api import APIFactory
from pytradfri import Gateway

aes = alarmevents.AES()

max_retry = 4

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns

table = sql_object("out_tradfri", "Outputs", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("hue","VARCHAR(45)"),("bri","VARCHAR(45)"),("sat","VARCHAR(45)"),("an","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))

identity = constants.tradfri_.identity
psk = constants.tradfri_.psk
host = constants.tradfri_.host
api_factory = APIFactory(host=host, psk_id=identity, psk=psk)
api = api_factory.request
gateway = Gateway()
devices_command = gateway.get_devices()
devices_commands = api(devices_command)
devices = api(devices_commands)
lights = [dev for dev in devices if dev.has_light_control]

class Tradfri_lights():
    def __init__(self):
        self.__init_table__()
    
    def __init_table__(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+table.name+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+table.name +"("
                for num, col in enumerate(table.columns):
                    if num == len(table.columns)-1:
                        for co in col:
                            command += co + " "
                        command +=  ");"
                    else:
                        for co in col:
                            command += co + " "                    
                        command +=  ", "
                cur.execute(command)
                results = cur.fetchall()      
        con.close()     
    
    def list_commands(self):
        comands = mysql_connector.mdb_get_table(table.name)
        liste = ['Umschalten']
        for comand in comands:
            liste.append(comand.get("Name"))
        liste.remove("Name")
        return liste

    def dict_commands(self):
        #comands = mdb_get_table(table.name)
        dicti = {'':1,'man':2,'auto':3}
        itera = 3
        liste = self.list_commands()
        for item in liste:
            itera +=1            
            dicti[str(item)] = itera
        return dicti  
        
    def list_devices(self):
        return  [l.name for l in lights]

    def get_light_by_name(self, name):
        for l in lights:
            if l.name == name:
                return l
        return None

    def set_device(self, device, commd):
        success = False
        szene = mysql_connector.mdb_read_table_entry(table.name,commd)
        
        if szene.get('bri')<=0 or not szene['on']:
            szene['bri'] = 0
        
        l = self.get_light_by_name(device)
        
        if l != None:
    #        dim_command = l.light_control.set_dimmer(szene['bri'])
    #        api(dim_command)
    
            color_command = l.light_control.set_hsb(szene['hue'], szene['sat'], szene['bri'])
            api(color_command)
            
            success = True
        
        return success
 