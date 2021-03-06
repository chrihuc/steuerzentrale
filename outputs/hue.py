#!/usr/bin/env python

import constants

from phue import Bridge, Light

import MySQLdb as mdb
import time

import logging
logging.basicConfig()

from database import mysql_connector
from alarm_event_messaging import alarmevents

from tools import toolbox
#toolbox.log(device, commd)

# TODO Tests split adress from hks

aes = alarmevents.AES()

max_retry = 4

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns

table = sql_object("out_hue", "Outputs", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("hue","VARCHAR(45)"),("bri","VARCHAR(45)"),("sat","VARCHAR(45)"),("an","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))

try:
    hbridge = Bridge(constants.hue_.IP)
    hbridge.connect()
except:
    print "Hue not connecting, press button."
    try:
        import easygui
        easygui.msgbox("Hue not connecting", title="press button")
    except:
        pass


class Hue_lights():
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
        lights = hbridge.lights
        return  [l.name for l in lights]


    def set_device(self, device, commd):
        toolbox.log(device, commd)
        h_dev = Light(hbridge, device)
        keys = ['bri', 'hue', 'sat', 'transitiontime']
        szene = mysql_connector.mdb_read_table_entry(table.name,commd)
        success = False
        if szene.get('bri')<=0:
            szene['bri'] = 0
            szene['on'] = False
        elif commd == 'Save': 
            hue = hbridge.get_light(device, 'hue')
            bri = hbridge.get_light(device, 'bri')
            sat = hbridge.get_light(device, 'sat')
            an = hbridge.get_light(device, 'on') 
            #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
            setting = {'hue': hue, 'bri': bri, 'sat': sat, 'an': an}
            mysql_connector.mdb_set_table(table.name,device, setting)
            return True
        elif commd == 'Umschalten':
            an = hbridge.get_light(device, 'on') 
            if an:
                szene['on'] = False
            else:
                szene['on'] = True
        elif commd == 'sz_toggle':
            an = hbridge.get_light(device, 'on') 
            if an:
                commd="SZ_Aus"
            else:
                szene['on'] = True
        bright = szene.get('bri')
        if bright <> None and bright>0:
            szene['bri'] = int(bright)
        if bright <> None and bright<=0:
            pass     
        # switch light on to be able to modify it
        if str(szene.get('on')) == "1" or str(szene.get('on')) == "True":
            try:         
                success = h_dev.on
            except:
                success = False
            retry = 1
            while not success and retry < max_retry:
                try:
                    hbridge.set_light(device, {'on':True}) 
                    success = h_dev.on
                except:
                    time.sleep(1)
                    success = False
                    retry += 1
            if not success:
                return success            
            time.sleep(0.5)
        command = {}
        for key in keys:
            if ((szene.get(key) <> "") and (str(szene.get(key)) <> "None")):
                command[key] = int(szene.get(key))
        # first get status then execute command
        t_sucess = False
        retry = 1
        t_h_dev = False
        while not t_sucess and retry < max_retry:
            try:
                t_h_dev = h_dev.on
                t_sucess = True
            except:
                time.sleep(retry * 1)
                t_sucess = False
                retry += 1
        if retry == max_retry:
            print(device, ' hue timed out')
        if command <> {} and t_h_dev:
            success = False
            retry = 1
            while not success and retry < max_retry:
                try:
                    hbridge.set_light(device, command)
                    success = True
                except:
                    time.sleep(1)
                    success = False 
                    retry += 1
        # switch light off
        if str(szene.get('on')) == "0" or str(szene.get('on')) == "False":
            success = False #not h_dev.on
            retry = 1
            if 'transitiontime' in command:
                if command['transitiontime'] > 0:
                    time.sleep(command['transitiontime']/10)
            while not success and retry < max_retry:
                try:
                    hbridge.set_light(device, {'on':False})  
                    success = not h_dev.on
                except:
                    time.sleep(1)
                    success = False 
                    retry += 1
            if retry == max_retry:
                print(device, ' hue timed out')
        try:
            if not h_dev.reachable:
                success = False
                aes.new_event(description=str(device) + " really not reachable", prio=1)
        except:
            success = False
            aes.new_event(description=str(device) + " not reachable", prio=1)            
        return success
 