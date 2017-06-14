#!/usr/bin/env python

import constants

import MySQLdb as mdb
from threading import Timer
import time
from time import localtime, strftime
import datetime

#import mysql.connector as sql 
#import pandas as pd

#db_connection = sql.connect(host='192.168.192.10', database='Steuerzentrale', user='customer', password='user')
#df = pd.read_sql('SELECT * FROM set_Szenen', con=db_connection)


datab = constants.sql_.DB

#auto add entry to inputs
#replace all dbs with constants
#rewrite defs at the end

def main():
    #print mdb_set_table(table=constants.sql_tables.cron.name, device='Wochentags1', commands={u'Do': True, u'Fr': True, 'Name': u'Wochentags1', u'Di': True, u'Eingeschaltet': True, u'Mo': True, u'Mi': True, u'So': False, 'Time': u'06:40', u'Sa': False, 'Szene': u'Wecker'}, primary = 'Name')
    #print setting_r("Notify_Christoph")
    #print re_calc(['lin_calc',[1,2,['lin_calc',[1,'temp',1]]]])
    #print re_calc(['lin_calc',[1,'temp',1]])
    #print re_calc(['sett','Temperatur_Wohnzi'])
    # print getSzenenSources('Webcam_aus')
    # print getSzenenSources('Webcam_aus')
    #print maxSzenenId()-maxSzenenId()%10 +10
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
    #values = {'Wach': None, 'Schlafen': None, 'Leise': None, 'Setting': 'True', 'last1': datetime.datetime(2016, 4, 11, 19, 14, 37), 'last2': datetime.datetime(2016, 4, 11, 19, 13, 48), 'Besuch': None, 'last_Value': decimal('16.90'), 'AmGehen': None, 'Description': 'Temperatur Terasse', 'Urlaub': None, 'Value_lt': None, 'Logging': 'True', 'Name': 'A00TER1GEN1TE01', 'Dreifach': None, 'Gegangen': None, 'Doppel': None, 'Value_eq': None, 'Value_gt': None, 'Abwesend': None, 'Schlummern': None, 'Id': 1L}
    #mdb_add_table_entry("test",values)
#    print str(mdb_get_table(constants.sql_tables.Besucher.name))
    print inputs('6De9SU.m4d','0')
#    mdb_add_table_entry('out_hue',{'Name':'Neuer Befehl'})
#    print mdb_read_table_entry(constants.sql_tables.szenen.name, 'AdvFarbWechsel')
#    print mdb_read_table_column(constants.sql_tables.szenen.name, 'Name')
#    print mdb_read_table_entry('Steuerzentrale.sat_TFLED', 'Ambience')    

    
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
    ''' set single setting
    '''
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
    ''' read single setting
    '''    
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
def mdb_read_table_entry(db, entry, column='Name',recalc=True):
    cmds = teg_raw_cmds(db)
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db + ' WHERE '+column+' = "' + str(entry) +'"'
        sql = 'SELECT * FROM %s WHERE %s = "%s"' % (db, column, str(entry))
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
                if len(cmds) == 0:
                    commando = field_names[i]
                else:
                    commando = cmds.get(field_names[i])  
                if recalc:
                    dicti[commando] = re_calc(row[i])
                    try:
                        old_dict = eval(row[i])
                        if isinstance(old_dict, dict):
                            print old_dict
                            new_dict = {}
                            for key, value in old_dict.iteritems(): 
                                new_dict[key] = re_calc(value)
                            dicti[commando] = new_dict
                    except:
                        pass
                    
                else:
                    dicti[commando] = (row[i]) 
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

def mdb_read_table_column_filt(db, column, filt='', amount=1000, order="desc", exact=False):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
        if exact:
            sql = 'SELECT '+column+' FROM ' + db + ' WHERE Name LIKE "' + filt + '" ORDER BY ID ' + order + ' LIMIT ' + str(amount) # % (column,db,filt,order, str(amount))
        else:
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

def mdb_add_table_entry(table, values, primary = 'Id'):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    listNames = []
    listValues = []
    strin = 'INSERT INTO %s (' % (table)
    for val in values:
        if val <> primary:
            strin += '%s, ' % (val)
            listNames.append(val)
            listValues.append(values.get(val))
    strin = strin[0:-2] +') VALUES ('
    for val in values:
        if val <> primary:
            strin += '"'+str(values.get(val)) + '", '    
    strin = strin[0:-2] + ')'
    with con:
        cur = con.cursor()  
        cur.execute(strin) 
    con.close() 

def get_raw_cmds(db):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM %s WHERE Name = "Name"' % (db)
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

           

#kompletter table:
def mdb_get_table(db):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM %s' % (db)
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

def mdb_set_table(table, device, commands, primary = 'Name', translate = False):
    ''' set table
        table = table name to change
        device = entry in table, if primary is name then where the name fits
        commands = columns in the table where "device" entry will be changed
        translate with this flag the commandos will be translated according to the raw commands table
    '''
    cmds = get_raw_cmds(table)
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SELECT COUNT(*) FROM %s.%s WHERE %s = "%s"' % (datab,table,primary,device)
        cur.execute(sql)
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+table+' ('+primary+') VALUES ("'+ str(device) + '")'     
            cur.execute(sql)   
        for cmd in commands:
            if (len(cmds) == 0) or not translate:
                commando = cmd
            else:
                commando = cmds.get(cmd)
            if str(commands.get(cmd)) == 'None':
                sql = 'UPDATE %s SET %s = NULL WHERE %s = "%s"' % (table, str(commando), primary, str(device))
            else:
                #sql = 'UPDATE '+table+' SET '+str(commando)+' = "'+str(commands.get(cmd))+ '" WHERE Name = "' + str(device) + '"'
                sql = 'UPDATE %s SET %s="%s" WHERE %s="%s"' % (table, (commando), commands.get(cmd), primary, (device))
            if commando <> primary:
#                print sql
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
    
def getSzenenSources(szene):
    if szene in ['', None]:
        return [],[]
    print szene, constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    ilist, slist = [], []
    with con:
        print 'connecting'
        cur = con.cursor()
        sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' where "'+szene+\
              '" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach)'
        sql = 'SELECT * FROM %s where "%s" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach)' % (constants.sql_tables.inputs.name, szene)      
        print 'executing', sql
        cur.execute(sql)
        print 'executed 1'
        results = cur.fetchall()
        print results
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]  
            ilist.append(dicti)
        sql = 'SELECT * FROM '+constants.sql_tables.szenen.name+' where Follows like "%'+szene+'%"'
        szene = "%" + szene + "%"
        sql = 'SELECT * FROM %s.%s where Follows like "%s"' % (datab, constants.sql_tables.szenen.name, szene)    
        print 'executing 2' , sql
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]  
            slist.append(dicti)           
    con.close()   
    print ilist, slist
    return ilist, slist
    
def maxSzenenId():
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    value = 0
    with con:
        cur = con.cursor()
        sql = "SELECT Id FROM Steuerzentrale.set_Szenen ORDER BY id DESC LIMIT 0, 1"
        cur.execute(sql)
        results = cur.fetchall()
    con.close()            
    return results[0][0]    
    
def inputs(device, value):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    dicti_1 = {}
    szenen = []  
    lt = datetime.datetime.now()
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"'")
        if cur.fetchone()[0] == 0:    
            sql = 'INSERT INTO '+constants.sql_tables.inputs.name+' (Name, HKS, Description, Logging, Setting, Doppelklick) VALUES ("' + str(device) + '","' + str(device) + '","' + str(device) + '","True","False","False")'
            cur.execute(sql)
        else:
#            get last value and last time
            sql = 'SELECT * FROM %s WHERE Name = "%s"' % (constants.sql_tables.inputs.name, str(device))
            cur.execute(sql)
            results_1 = cur.fetchall()
            field_names_1 = [i[0] for i in cur.description]    
            for row in results_1:
                for i in range (0,len(row)):
                    dicti_1[field_names_1[i]] = row[i] 
            last_value = dicti_1['last_Value']
            last_time = dicti_1['last1']
            if str(last_time) == 'None': last_time = lt
            deltaT = lt - last_time
            deltaTm = deltaT.total_seconds() / 60
            if deltaTm > 0:
                deltaX = float(value) - float(last_value)
                gradient = deltaX #/ deltaTm
            else:
                gradient = float(value) - float(last_value)
            sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET Gradient = "'+str(gradient)+'" WHERE Name = "' + str(device) +'"'
            cur.execute(sql)              
            
            sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' WHERE Name = "' + str(device) +'"'
            value = str(value)
            sql2 = ' AND ((Value_lt > "' + value + '" OR Value_lt is NULL )'
            sql2 = sql2 + ' AND (Value_eq = "' + value  + '" OR Value_eq is NULL )'
            sql2 = sql2 + ' AND (Value_gt < "' + value  + '" OR Value_gt is NULL )'
            sql2 = sql2 + ' AND (Gradient_lt > "' + str(gradient) + '" OR Gradient_lt is NULL )'
            sql2 = sql2 + ' AND (Gradient_gt < "' + str(gradient) + '" OR Gradient_gt is NULL )'
            sql2 = sql2 + ');' 
            cur.execute(sql + sql2)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            for row in results:
                single = True
                for i in range (0,len(row)):
                    dicti[field_names[i]] = row[i]  
                doppelklick = dicti.get("Doppelklick")
                if str(dicti.get("last2")) <> "None":             
                    if lt - dicti.get("last2") < datetime.timedelta(hours=0, minutes=0, seconds=4):
                        szenen.append(dicti.get("Dreifach")) 
                        single = False
                    elif lt - dicti.get("last1") < datetime.timedelta(hours=0, minutes=0, seconds=3):
                        szenen.append(dicti.get("Doppel"))     
                        single = False
                if str(doppelklick) <> "True": single = True
                if single: szenen.append(dicti.get(setting_r("Status"))) 
                szenen.append(dicti.get('Immer'))
            try:
                hks = dicti['HKS']
                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Setting = 'True'")
                if cur.fetchone()[0] > 0: 
                    setting_s(hks, value)
                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Logging = 'True'")
                if cur.fetchone()[0] > 0: 
                    insertstatement = 'INSERT INTO '+constants.sql_tables.his_inputs.name+'(Name, Value, Date) VALUES("' + str(hks) + '",' + str(value) + ', NOW())'
                    cur.execute(insertstatement) 
                    insertstatement = 'INSERT INTO '+constants.sql_tables.his_inputs.name+'(Name, Value, Date) VALUES("' + str(hks) + '_grad",' + str(gradient) + ', NOW())'
                    cur.execute(insertstatement)
            except:
                pass
            sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last1 = "'+str(lt)+'" WHERE Name = "' + str(device) +'"'
            cur.execute(sql)               
            if str(dicti.get("last1")) <> "None":
                sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last2 = "'+str(dicti.get("last1"))+'" WHERE Name = "' + str(device) +'"'
                cur.execute(sql + sql2)            
                
        sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last_Value = "'+str(value)+'" WHERE Name = "' + str(device) +'"'
        cur.execute(sql)                 
    con.close()
    return szenen
        
if __name__ == '__main__':
    main()    