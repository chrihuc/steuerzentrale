#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

#!/usr/bin/env python

import constants

import MySQLdb as mdb
import time
import uuid

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

class NoKey(Exception):
    pass

def authenticate():
    identity = uuid.uuid4().hex
    api_factory = APIFactory(host=constants.tradfri_.host, psk_id=identity)
    if constants.tradfri_.key == '':
        aes.new_event(description="Kein Key für Tradfri", prio=9)
        raise KeyError
    psk = api_factory.generate_psk(constants.tradfri_.key) 
    constants.tradfri_.identity = identity
    constants.tradfri_.psk = psk
    constants.config.set('TRADFRI', 'Identity', identity)
    constants.config.set('TRADFRI', 'PSK', psk)
    constants.config.set('TRADFRI', 'Key', '')
    constants.save_config()
    return api_factory
    
identity = constants.tradfri_.identity
psk = constants.tradfri_.psk
host = constants.tradfri_.host
if psk == '' or identity == '':
    api_factory = authenticate()
else:
    api_factory = APIFactory(host=host, psk_id=identity, psk=psk)
api = api_factory.request
try:
    gateway = Gateway()
    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]
except:
    devices_command = []
    devices_commands = []
    devices = []
    lights = []
    aes.new_event(description="Tradfri nicht erreichbar", prio=9)
    
#for l in lights:
#    print(l.light_control.can_set_color)

class Tradfri_lights():
    
    locklist = {}
    
    def __init__(self):
        self.devices = self.list_devices()
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
#        liste.remove("Name")
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
        liste = []
        for l in lights:
            if name in l.name:
                liste.append(l)
        if liste:
            return liste
        else:
            return None

    def set_device(self, device, commd):
        success = False
        szene = mysql_connector.mdb_read_table_entry(table.name,commd)
        
        if int(szene.get('bri'))<=0 or not szene['an']:
            bri = 0
        else:
            bri = min(int(szene['bri']), 254)
        
        l = self.get_light_by_name(device)
        if szene['temp'] == None:
            temp = 454 # 250 454
        else:
            temp = int(szene['temp'])
         
        if szene['transitiontime'] is not None:
            transT = int(szene['transitiontime'])
        else:
            transT = 0
#        print(transT)
        
        if l != None:
    #        dim_command = l.light_control.set_dimmer(szene['bri'])
    #        api(dim_command)
#            print(l)
            for lampe in l:
                hash_id = str(uuid.uuid4())
                Tradfri_lights.locklist[lampe] = hash_id
                if bri == 0:
                    dim_command = lampe.light_control.set_dimmer(bri, transition_time=transT)
                    self.api_cmd(dim_command)
                elif transT == 0:
                    if lampe.light_control.can_set_color:                     
    #                    RANGE_SATURATION = (0, 65279)
                        color_command = lampe.light_control.set_hsb(int(szene['hue']), int(szene['sat']))
                        self.api_cmd(color_command)
                        dim_command = lampe.light_control.set_dimmer(bri)
                        self.api_cmd(dim_command)                    
                    else:
                        dim_command = lampe.light_control.set_dimmer(bri)
                        self.api_cmd(dim_command) 
                        dim_command = lampe.light_control.set_color_temp(temp)
                        self.api_cmd(dim_command)
                else:
                    if lampe.light_control.can_set_color:                     
    #                    RANGE_SATURATION = (0, 65279)
                        color_command = lampe.light_control.set_hsb(int(szene['hue']), int(szene['sat']), brightness=bri, transition_time=transT*10)
                        self.api_cmd(color_command)
                        time.sleep(transT + 5)
                        if Tradfri_lights.locklist[lampe] == hash_id:
                            color_command = lampe.light_control.set_hsb(int(szene['hue']), int(szene['sat']), brightness=bri, transition_time=transT*10)
                            self.api_cmd(color_command)
#                        dim_command = lampe.light_control.set_dimmer(bri, transition_time=transT)
#                        api(dim_command)                    
                    else:
                        dim_command = lampe.light_control.set_color_temp(temp)
                        self.api_cmd(dim_command)
                        time.sleep(1)
                        if Tradfri_lights.locklist[lampe] == hash_id:                         
                            dim_command = lampe.light_control.set_dimmer(bri, transition_time=transT*10)
                            self.api_cmd(dim_command) 
            success = True
        return success
    
    def api_cmd(self, command):
        retry_max = 3
        retry = 0
        while retry < retry_max:
            try:
                api(command)
                retry = retry_max
            except:
                retry += 1
                time.sleep(0.05 * retry)
                if retry >= retry_max:
                    print("Tradfri max retries reached")