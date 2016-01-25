#!/usr/bin/env python

import constants

from mysql_con import mdb_set_table, mdb_read_table_entry,set_val_in_szenen,mdb_get_table
from phue import Bridge

import MySQLdb as mdb
import time

import logging
logging.basicConfig()

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns

table = sql_object("out_hue", "Outputs", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("hue","VARCHAR(45)"),("bri","VARCHAR(45)"),("sat","VARCHAR(45)"),("an","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))

hbridge = Bridge(constants.hue_.IP)

def main():
    hue_l = hue_lights()
    hue_l.set_device("Stablampe_2", "Rot")
    #print hue_l.list_devices()
    
class hue_lights():
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
        comands = mdb_get_table(table.name)
        liste = []
        for comand in comands:
            liste.append(comand.get("Name"))
        liste.remove("Name")
        return liste

    def list_devices(self):
        comands = mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
        liste = []
        for comand in comands:
            if comands.get(comand) == "HUE":
                liste.append(comand)
        #liste.remove("Name")
        return liste

    def set_device(self, device, commd):
        keys = ['bri', 'hue', 'sat', 'transitiontime']
        szene = mdb_read_table_entry(table.name,commd)
        if commd in ["man", "auto"]:
            set_val_in_szenen(device=device, szene="Auto_Mode", value=commd)
            return
        elif commd == 'Save': 
            hue = hbridge.get_light(device, 'hue')
            bri = hbridge.get_light(device, 'bri')
            sat = hbridge.get_light(device, 'sat')
            an = hbridge.get_light(device, 'on') 
            #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
            setting = {'hue': hue, 'bri': bri, 'sat': sat, 'an': an}
            mdb_set_table(table.name,device, setting)
            return
        elif commd == 'toggle':
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
        if szene.get('bri') <> None:
            szene['bri'] = int(szene.get('bri'))
        if str(szene.get('on')) == "1" or str(szene.get('on')) == "True":
            hbridge.set_light(device, {'on':True}) 
            #time.sleep(0.5)
        command = {}
        for key in keys:
            if ((szene.get(key) <> "") and (str(szene.get(key)) <> "None")):
                command[key] = int(szene.get(key))
        if command <> {}:
            hbridge.set_light(device, command)
        if str(szene.get('on')) == "0" or str(szene.get('on')) == "False":
            hbridge.set_light(device, {'on':False})  
        set_val_in_szenen(device=device, szene="Value", value=szene.get('on'))
        return True

if __name__ == '__main__':
    main()  