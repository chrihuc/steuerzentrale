#!/usr/bin/env python

import constants

import MySQLdb as mdb
from threading import Timer
import time
from time import localtime, strftime
import datetime

datab = constants.sql_.DB

#auto add entry to inputs
#replace all dbs with constants
#rewrite defs at the end

def main():
    print mdb_get_table(db='set_Szenen')
    #print setting_r("Notify_Christoph")
    #print re_calc(['lin_calc',[1,2,['lin_calc',[1,'temp',1]]]])
    #print re_calc(['lin_calc',[1,'temp',1]])
    #print re_calc(10)
    #set_automode(device="Stehlampe", mode="auto")
    #print mdb_szene_r("Device_Typ")
    #typ_dict = mdb_szene_r("Device_Typ")
    #ezcontrol_devices = []
    #TF_LEDs = []
    #hue_devices = []
    #for device in typ_dict:
        #if typ_dict.get(device) == "EZControl":
            #ezcontrol_devices.append(device)
        #if typ_dict.get(device) == "TF_LEDs":
            #TF_LEDs.append(device)
        #if typ_dict.get(device) == "Hue":
            #hue_devices.append(device)            
    #print hue_devices

def re_calc(inpt):
    #['lin_calc',[1,'temp',1]]
    #['lin_calc',[1,2,['lin_calc',[1,'temp',1]]]]
    #['sett','Temperatur_Balkon']
    if "calc" in str(inpt):
        try:
            if type(eval(str(inpt))) == list:
                lst = eval(str(inpt))
                for num, sub in enumerate(lst[1]):
                    if "calc" in str(sub):
                        lst[1][num] = re_calc(sub)
                    elif type(sub) == str:
                        lst[1][num] = float(setting_r(lst[1][num]))
                if lst[0] == "lin_calc":
                    return (lst[1][0] * lst[1][1]) + lst[1][2]
        except:
            return inpt
    if "sett" in str(inpt): 
        lst = eval(str(inpt))  
        if lst[0] == "sett":
            return float(setting_r(lst[1]))
        else:
            for num, sub in enumerate(lst):
                if "sett" in str(sub):
                    lst[num] = re_calc(sub)
            return lst
    else:
        return inpt
       
def setting_s(setting, wert):
    if wert in ('Ein','ein','an'):
        wert = True
    if wert in ('Aus','aus'):
        wert = False
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.settings.name+" WHERE Name = '"+setting+"'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+constants.sql_tables.settings.name+' (Value, Name) VALUES ("' + str(wert) + '","'+ str(setting) + '")'
        else:
            sql = 'UPDATE '+constants.sql_tables.settings.name+' SET Value = "' + str(wert) + '" WHERE Name = "'+ str(setting) + '"'
        cur.execute(sql)
    con.close() 
    
def setting_r(setting):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    value = 0
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.settings.name+" WHERE Name = '"+setting+"'")
        if cur.fetchone()[0] == 0:   
            sql = 'INSERT INTO '+constants.sql_tables.settings.name+' (Value, Name) VALUES (0,"'+ str(setting) + '")'
            value = 0
            cur.execute(sql)
        else:
            sql = 'SELECT * FROM '+constants.sql_tables.settings.name+' WHERE Name = "' + str(setting) +'"'
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                fname = row[1]
                value = row[2]
    con.close()            
    return value

def settings_r():
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM '+constants.sql_tables.settings.name
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti[row[1]] = row[2]            
    con.close()    
    return dicti 

def set_val_in_szenen(device, szene, value):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SET SQL_SAFE_UPDATES = 0'
        cur.execute(sql)        
        sql = 'UPDATE '+constants.sql_.DB+'.'+constants.sql_tables.szenen.name+' SET '+device+' = "' + str(value) + '" WHERE Name = "' + str(szene) + '"'
        cur.execute(sql)
    con.close()                   

## alle mit dicti:
def mdb_read_table_entry(db, entry):
    cmds = teg_raw_cmds(db)
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db + ' WHERE Name = "' + str(entry) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
                if len(cmds) == 0:
                    commando = field_names[i]
                else:
                    commando = cmds.get(field_names[i])                
                dicti[commando] = re_calc(row[i])            
    con.close()    
    return dicti       

def mdb_read_table_column(db, column):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        sql = 'SELECT '+column+' FROM ' + db
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            rlist.append(row[0])
    con.close()    
    return rlist 

def mdb_read_table_column_filt(db, column, filt='', amount=1000, order="desc"):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
        sql = 'SELECT '+column+' FROM ' + db + ' WHERE Name LIKE "%' + filt + '%" ORDER BY ID ' + order + ' LIMIT ' + str(amount)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            if type(row[0]) == datetime.datetime:
                rlist.append((int(row[0].strftime("%s"))))
            else:
                rlist.append(eval(str(row[0])))
    con.close()    
    return rlist 

def get_raw_cmds(db):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db + ' WHERE Name = "Name"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               dicti[row[i]] = field_names[i]            
    con.close()    
    return dicti

def teg_raw_cmds(db):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db + ' WHERE Name = "Name"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               dicti[field_names[i]] =  row[i]           
    con.close()
    return dicti
#def mdb_sideb_r(name):
    #return mdb_read_table_entry('Sideboard', name) 

#def mdb_marantz_r(name):
    #return mdb_read_table_entry('Marantz', name) 
        
#def mdb_ls_sz_r(name):
    #return mdb_read_table_entry('LightstrSchlafzi', name)    

#def hue_autolicht(name):
    #return mdb_read_table_entry('hue_autolicht', name)  
    
#def mdb_szene_r(name):
    #return mdb_read_table_entry('Szenen', name)       
        
#def mdb_hue_r(name):
    #return mdb_read_table_entry('Hue', name)

#def mdb_tspled_r(name):
    #return mdb_read_table_entry('TuerSPiLED', name) 
    
#def mdb_sonos_r(player):
    #return mdb_read_table_entry('Sonos', player) 
           

#kompletter table:
def mdb_get_table(db):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]  
            rlist.append(dicti)
    con.close()    
    return rlist  

def mdb_set_table(table, device, commands):
    cmds = get_raw_cmds(table)
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+table+" WHERE Name = '"+device+"'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+table+' (Name) VALUES ("'+ str(device) + '")'     
            cur.execute(sql)   
        for cmd in commands:
            if len(cmds) == 0:
                commando = cmd
            else:
                commando = cmds.get(cmd)
            sql = 'UPDATE '+table+' SET '+str(commando)+' = "'+str(commands.get(cmd))+ '" WHERE Name = "' + str(device) + '"'
            cur.execute(sql)       
    con.close() 

#def mdb_sonos_s(player, commands):
    ##commands = Pause, Radio, Sender, TitelNr, Time, MasterZone, Volume
    #if player in sn.Names:
        #playern = sn.Names.get(player)
    #else:
        #playern = player
    #cmds = get_raw_cmds(constants.sql_tables.Sonos.name)
    #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    #with con:
        #cur = con.cursor()
        #for cmd in commands:
            #if len(cmds) == 0:
                #commando = cmd
            #else:
                #commando = cmds.get(cmd)
            #sql = 'UPDATE '+constants.sql_tables.Sonos.name+' SET '+str(commando)+' = "'+commands.get(cmd)+ '" WHERE Name = "' + str(playern) + '"'
            #cur.execute(sql)       
    #con.close()          
    
#def mdb_hue_s(device, commands):
    ##setting must be a dict
    ##{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
    #cmds = get_raw_cmds(constants.sql_tables.hue.name)
    #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    #with con:
        #cur = con.cursor()
        #for cmd in commands:
            #if len(cmds) == 0:
                #commando = cmd
            #else:
                #commando = cmds.get(cmd)            
            #sql = 'UPDATE '+constants.sql_tables.hue.name+' SET '+str(commando)+' = "'+commands.get(cmd)+ '" WHERE Name = "' + str(device) + '"'
            #print sql
            #cur.execute(sql)  
    #con.close()       
        
##to rewrite  

#def mdb_marantz_s(name, setting):
    ##setting must be a dict
    ##{'Treble': '7', 'Bass': '2', 'Power': 'True', 'Mute': 'False', 'Attenuate': 'False', 'Volume': '-25', 'Source': '11'}
    #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    #with con:
        #cur = con.cursor()
        #sql = "UPDATE Marantz SET Power = '" + str(setting.get("Power")) + "', Volume = '0" + str(setting.get("Volume")) + "', Source = '" + str(setting.get("Source")) + "', Mute = '" + str(setting.get("Mute")) + "' WHERE Name = '" + name +"'"
        #cur.execute(sql) 
    #con.close()        
        
#def mdb_sideb_s(name, setting):
    ##setting must be a dict
    ##{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
    #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    #with con:
        #cur = con.cursor()
        #sql = "UPDATE Sideboard SET rot = '" + str(setting.get("rot")) + "', gruen = '" + str(setting.get("gruen")) + "', blau = '" + str(setting.get("blau")) + "' WHERE Name = '" + name +"'"
        #cur.execute(sql)     
    #con.close() 
    
def inputs(device, value):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    szenen = []  
    lt = datetime.datetime.now()
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Input = '"+device+"'")
        if cur.fetchone()[0] == 0:    
            sql = 'INSERT INTO '+constants.sql_tables.inputs.name+' (Input, Logging) VALUES ("' + str(device) + '",1)'
            cur.execute(sql)
        else:
            sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' WHERE Input = "' + str(device) +'"'
            value = str(value)
            sql2 = ' AND ((Value_lt > "' + value + '" OR Value_lt is NULL )'
            sql2 = sql2 + ' AND (Value_eq = "' + value  + '" OR Value_eq is NULL )'
            sql2 = sql2 + ' AND (Value_gt < "' + value  + '" OR Value_gt is NULL )'
            sql2 = sql2 + ');' 
            cur.execute(sql + sql2)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            for row in results:
                single = True
                for i in range (0,len(row)):
                    dicti[field_names[i]] = row[i]                     
                if str(dicti.get("last2")) <> "None":             
                    if lt - dicti.get("last2") < datetime.timedelta(hours=0, minutes=0, seconds=4):
                        szenen.append(dicti.get("Dreifach")) 
                        single = False
                    elif lt - dicti.get("last1") < datetime.timedelta(hours=0, minutes=0, seconds=3):
                        szenen.append(dicti.get("Doppel"))     
                        single = False
                if single: szenen.append(dicti.get(setting_r("Status")))         
            sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last1 = "'+str(lt)+'" WHERE Input = "' + str(device) +'"'
            cur.execute(sql + sql2)          
            if str(dicti.get("last1")) <> "None":
                sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last2 = "'+str(dicti.get("last1"))+'" WHERE Input = "' + str(device) +'"'
                cur.execute(sql + sql2)            
            cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Input = '"+device+"' AND Setting = 1")
            if cur.fetchone()[0] > 0: 
                setting_s(device, value)
            cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Input = '"+device+"' AND Logging = '1'")
            if cur.fetchone()[0] > 0: 
                insertstatement = 'INSERT INTO '+constants.sql_tables.his_inputs.name+'(Name, Value, Date) VALUES("' + str(device) + '",' + str(value) + ', NOW())'
                cur.execute(insertstatement) 
    con.close()
    return szenen
        
if __name__ == '__main__':
    main()    