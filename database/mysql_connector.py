#!/usr/bin/env python

import pandas as pd

import constants

import MySQLdb as mdb
import warnings
warnings.filterwarnings('ignore', category=mdb.Warning)
from threading import Timer
import time
from time import localtime, strftime
import datetime
from outputs.mqtt_publish import mqtt_pub
#import json

# TODO: reconnect of MQTT

#client = mqtt.Client(constants.name + '_mysql_con')
#client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
#client.connect(constants.mqtt_.server)
#client.loop_start()
datab = constants.sql_.DB

validTimers = {}
locklist = {}

class tables(object):
# TODO: change table names to constant settings
#    db_connection = sql.connect(host=constants.sql_.IP,
#                                database=constants.sql_.DB,
#                                user=constants.sql_.USER,
#                                password=constants.sql_.PASS)
    db_connection = mdb.connect(constants.sql_.IP, constants.sql_.USER,
                                constants.sql_.PASS, constants.sql_.DB)
#    warnings.filterwarnings('ignore', 'Unknown table .*')
    scenes_df = pd.read_sql('SELECT * FROM set_Szenen', con=db_connection)
    _lines = ['Adress', 'Device_Type', 'Description', 'Auto_Mode', 'Command_Table']
    aktors_df = scenes_df.loc[scenes_df['Name'].isin(_lines)].set_index('Name')
    akt_types = constants.akt_types
    akt_type_dict = {typ:[] for typ in akt_types}
    aktors_dict = aktors_df.to_dict()
    for aktor in aktors_dict:
        if aktors_dict[aktor]['Device_Type'] in akt_types:
            akt_type_dict[aktors_dict[aktor]['Device_Type']].append(aktor)
    akt_adr_dict = aktors_df[aktors_df.index == 'Adress'].to_dict(orient='records')[0]
    akt_cmd_tbl_dict = aktors_df[aktors_df.index == 'Command_Table'].to_dict(orient='records')[0]
    inputs_df = pd.read_sql('SELECT * FROM cmd_inputs', con=db_connection)
    inputs_df.fillna(value=0, inplace=True)
    db_connection.close()
    _inputs_dict = inputs_df.to_dict(orient='records')
    inputs_dict = {}
    for item in _inputs_dict:
        inputs_dict[item['Name']] = item
    inputs_dict_hks = {}
    for item in _inputs_dict:
        inputs_dict_hks[item['HKS']] = item

    @classmethod
    def reload_scenes(cls):
#        db_connection = sql.connect(host=constants.sql_.IP,
#                                database=constants.sql_.DB,
#                                user=constants.sql_.USER,
#                                password=constants.sql_.PASS)
        db_connection = mdb.connect(constants.sql_.IP, constants.sql_.USER,
                                    constants.sql_.PASS, constants.sql_.DB)
        cls.scenes_df = pd.read_sql('SELECT * FROM set_Szenen', con=db_connection)
        db_connection.close()

    @classmethod
    def reload_inputs(cls):
#        db_connection = sql.connect(host=constants.sql_.IP,
#                                database=constants.sql_.DB,
#                                user=constants.sql_.USER,
#                                password=constants.sql_.PASS)
        db_connection = mdb.connect(constants.sql_.IP, constants.sql_.USER,
                                    constants.sql_.PASS, constants.sql_.DB)
        inputs_df = pd.read_sql('SELECT * FROM cmd_inputs', con=db_connection)
        db_connection.close()
        inputs_df.fillna(value=0, inplace=True)
        _inputs_dict = inputs_df.to_dict(orient='records')
        cls.inputs_dict = {}
        for item in _inputs_dict:
            cls.inputs_dict[item['Name']] = item
        inputs_dict_hks = {}
        for item in _inputs_dict:
            cls.inputs_dict_hks[item['HKS']] = item



#auto add entry to inputs
#replace all dbs with constants
#rewrite defs at the end
#def handler(obj):
#    if hasattr(obj, 'isoformat'):
#        return obj.isoformat()
#    elif isinstance(obj, datetime.timedelta):
#        return obj.seconds
#    else:
#        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def re_calc(inpt):
    #['lin_calc',[1,'temp',1]]
    #['lin_calc',[1,2,['lin_calc',[1,'temp',1]]]]
    #['sub_calc',[20,['lin_calc',[0.5,'A00TER1GEN1TE01',0]]]] : 20-0.5*A00TER1GEN1TE01
    #['sett','Temperatur_Balkon']
    if "calc" in str(inpt):
        try:
#        if True:
            if type(eval(str(inpt))) == list:
                lst = eval(str(inpt))
                for num, sub in enumerate(lst[1]):
                    if "calc" in str(sub):
                        lst[1][num] = re_calc(sub)
                    elif type(sub) == str:
                        value = setting_r(lst[1][num])
                        lst[1][num] = float(value)
                if lst[0] == "lin_calc":
                    return (lst[1][0] * lst[1][1]) + lst[1][2]
                elif lst[0] == "add_calc":
                    return lst[1][0] + lst[1][1]
                elif lst[0] == "sub_calc":
                    return lst[1][0] - lst[1][1]                
        except:
            return inpt
    if "sett" in str(inpt):
        lst = eval(str(inpt))
        if lst[0] == "sett":
            value = setting_r(lst[1])
            return float(value)
        else:
            for num, sub in enumerate(lst):
                if "sett" in str(sub):
                    lst[num] = re_calc(sub)
            return lst
    else:
        return inpt

def get_input_value(hks):
    """ returns the value from an input device
    """
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    value = None
    with con:
        cur = con.cursor()
        cur.execute("SELECT last_Value FROM %s.%s WHERE HKS = '%s'" % (datab, constants.sql_tables.inputs.name, hks))
#        if cur.fetchone()[0] != 0:
#            con.close()
#            return False
        results = cur.fetchall()
        for row in results:
            value = row[0]
    con.close()
    return value

def inputs_r():
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT HKS, last_Value FROM '+constants.sql_tables.inputs.name
        cur.execute(sql)
        results = cur.fetchall()
#        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti[row[0]] = str(row[1])
    con.close()
    return dicti

def setting_s(setting, wert):
    ''' set single setting
    '''
    if wert in ('Ein','ein','an'):
        wert = True
    if wert in ('Aus','aus'):
        wert = False
    data = {'Value':wert, 'Setting':setting}
    mqtt_pub("Settings/" + setting, data)
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
    ''' try to read the setting from inputs table if not an input
        read single setting
    '''
    value = get_input_value(setting)
    if value is None:
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        value = 0
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.settings.name+" WHERE Name = '"+setting+"'")
            if cur.fetchone()[0] == 0:
                return False
                sql = 'INSERT INTO '+constants.sql_tables.settings.name+' (Value, Name) VALUES (0,"'+ str(setting) + '")'
                value = 0
                cur.execute(sql)
            else:
                sql = 'SELECT * FROM '+constants.sql_tables.settings.name+' WHERE Name = "' + str(setting) +'"'
                cur.execute(sql)
                results = cur.fetchall()
                for row in results:
#                    fname = row[1]
                    value = row[2]
        con.close()
    return value

def settings_r_old():
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM '+constants.sql_tables.settings.name
        cur.execute(sql)
        results = cur.fetchall()
#        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti[row[1]] = row[2]
    con.close()
    return dicti

def settings_r():
    dicti = settings_r_old()
    #dicti.update(inputs_r())
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
#        sql = 'SELECT * FROM ' + db + ' WHERE '+column+' = "' + str(entry) +'"'
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
                            new_dict = {}
                            for key, value in old_dict.items():
                                new_dict[key] = re_calc(value)
                            dicti[commando] = new_dict
                    except:
                        pass

                else:
                    dicti[commando] = (row[i])
    con.close()
    return dicti

def get_actor_value(hks):
    temp_res = mdb_read_table_entry(constants.sql_tables.szenen.name, 'Value')
    return temp_res[hks]

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

def mdb_read_table_columns(db, columns):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    liste = []
    with con:
        cur = con.cursor()
        column  = ''
        for col in columns[0:-1]:
            column = column + col + ', '
        column = column + columns[-1]
        sql = 'SELECT '+column+' FROM ' + db
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]
            liste.append(dicti)
    con.close()
    return liste

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
        if val != primary:
            strin += '%s, ' % (val)
            listNames.append(val)
            listValues.append(values.get(val))
    strin = strin[0:-2] +') VALUES ('
    for val in values:
        if val != primary:
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
            if commando != primary:
                cur.execute(sql)
    con.close()

def remove_entry(table, device, primary = 'Name'):
    ''' remove line
        table = table name to change
        device = entry in table, if primary is name then where the name fits
    '''
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SELECT COUNT(*) FROM %s.%s WHERE %s = "%s"' % (datab,table,primary,device)
        cur.execute(sql)
        if cur.fetchone()[0] == 0:
            con.close()
            return True
        sql = 'DELETE FROM %s.%s WHERE %s = "%s"' % (datab,table,primary,device)
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

def get_device_adress(device):
    """ returns the adress with with the device is saved in each interface
    """
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    value = 0
    with con:
        cur = con.cursor()
        cur.execute("SELECT %s FROM %s.%s WHERE ID = '6'" % (device, datab, constants.sql_tables.szenen.name))
#        if cur.fetchone()[0] != 0:
        results = cur.fetchall()
        for row in results:
            value = row[0]
    con.close()
    return value


def getSzenenSources(szene):
    if szene in ['', None]:
        return [],[]
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    ilist, slist = [], []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' where "'+szene+\
              '" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach, Alarm)'
        sql = 'SELECT * FROM %s where "%s" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach, Alarm)' % (constants.sql_tables.inputs.name, szene)
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]
            ilist.append(dicti)
        sql = 'SELECT * FROM '+constants.sql_tables.szenen.name+' where Follows like "%'+szene+'%"'
        szene = "%" + szene + "%"
        sql = 'SELECT * FROM %s.%s where Follows like "%s"' % (datab, constants.sql_tables.szenen.name, szene)
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]
            slist.append(dicti)
    con.close()
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

def inputs(device, value, add_to_mqtt=True):
#    i = 0
    ct = datetime.datetime.now()
    try:
        last_time = locklist[device]
    except KeyError:
        last_time = None
        locklist[device] = ct    
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    dicti_1 = {}
    szenen = []
    desc = None
    heartbt = None
    filtered = False
#    print(device,value)
#    if 'MQTT' in device:
#        add_to_mqtt = False
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
            
            # Filtern, wenn grösser oder kleiner Messung ignorieren
            filtering = dicti_1['Filter']
            try:
                filtering = eval(filtering)
            except:
                filtering = [None, None]
            if filtering[0]:
                if float(value) <= filtering[0]:
                    filtered = True
            if filtering[1]:
                if float(value) >= filtering[1]:
                    filtered = True
                    
            if not filtered:
                if last_value is None: last_value = value
                if not last_time:
                    try:
                        last_time = dicti_1['last1']
                    except:
                        last_time = ct - datetime.timedelta(hours=1)
                debounce = dicti_1['debounce']
                heartbt = dicti_1['heartbeat']
                desc = dicti_1['Description']
                if str(last_time) == 'None': last_time = ct - datetime.timedelta(hours=1)
                if debounce is None:
                    db_time = ct
                else:
                    db_time = last_time + datetime.timedelta(seconds=debounce)
    #                print('input debouncing ', ct, db_time)
                if ct >= db_time:
                    locklist[device] = ct
                deltaT = ct - last_time
                deltaTm = deltaT.total_seconds() / 60
                if deltaTm > 0:
                    deltaX = float(value) - float(last_value)
                    gradient = deltaX #/ deltaTm
                else:
                    gradient = float(value) - float(last_value)
                sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET Gradient = "'+str(gradient)+'" WHERE Name = "' + str(device) +'"'
    #            cur.execute(sql)
    
                sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' WHERE Name = "' + str(device) +'"'
                value = str(value)
#                sql2 = ' AND ((Value_lt > "' + value + '" OR Value_lt is NULL )'
#                sql2 = sql2 + ' AND (Value_eq = "' + value  + '" OR Value_eq is NULL )'
#                sql2 = sql2 + ' AND (Value_gt < "' + value  + '" OR Value_gt is NULL )'
    #            sql2 = sql2 + ' AND (Gradient_lt > "' + str(gradient) + '" OR Gradient_lt is NULL )'
    #            sql2 = sql2 + ' AND (Gradient_gt < "' + str(gradient) + '" OR Gradient_gt is NULL )'
                sql2 =  ' AND (enabled = "True" OR enabled is NULL)'
                sql2 = sql2 + ';'
#                print(sql2)
                cur.execute(sql + sql2)
                results = cur.fetchall()
                field_names = [i[0] for i in cur.description]
                #dicti = {key: "" for (key) in szene_columns}
                for row in results:
                    single = True
                    for i in range (0,len(row)):
                        dicti[field_names[i]] = row[i]
                    doppelklick = dicti.get("Doppelklick")
                    if ct >= db_time:
                        append = True
                        if str(dicti.get("last2")) != "None":
                            if ct - dicti.get("last2") < datetime.timedelta(hours=0, minutes=0, seconds=4):
                                szenen.append(dicti.get("Dreifach"))
                                single = False
                            elif ct - dicti.get("last1") < datetime.timedelta(hours=0, minutes=0, seconds=3):
                                szenen.append(dicti.get("Doppel"))
                                single = False
                        if str(doppelklick) != "True": single = True
                        if (dicti['Value_lt'] is not None and float(re_calc(dicti['Value_lt'])) <= float(value)):
                            append = False
                        if (dicti['Value_eq'] is not None and float(re_calc(dicti['Value_eq'])) != float(value)):
                            append = False
                        if (dicti['Value_gt'] is not None and float(re_calc(dicti['Value_gt'])) >= float(value)):
                            append = False
                        # Gradient
                        if (dicti['Gradient_lt'] is not None and float(re_calc(dicti['Gradient_lt'])) <= gradient):
                            append = False
#                        if (dicti['Gradient_eq'] is not None and float(re_calc(dicti['Gradient_eq'])) != gradient):
#                            append = False
                        if (dicti['Gradient_gt'] is not None and float(re_calc(dicti['Gradient_gt'])) >= gradient):
                            append = False                        
                        if single and append and dicti.get(setting_r("Status")) is not None: 
                            szenen.append(dicti.get(setting_r("Status")))
                        if append and dicti.get('Immer') is not None:szenen.append(dicti.get('Immer'))
    #            get stting and logging
                hks = dicti_1['HKS']
                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Setting = 'True'")
                if cur.fetchone()[0] > 0:
                    setting_s(hks, value)
                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Logging = 'True'")
                if cur.fetchone()[0] > 0 and str(hks) != str(device):
                    try:
                        insertstatement = 'INSERT INTO %s (%s, Date) VALUES(%s, NOW())' % (constants.sql_tables.his_inputs.name, hks, value)
                        cur.execute(insertstatement)
                    except:
                        try:
                            ist = "ALTER TABLE `%s` ADD `%s` DECIMAL(8,3)" % (constants.sql_tables.his_inputs.name, hks)
                            cur.execute(ist)
                            insertstatement = 'INSERT INTO %s (%s, Date) VALUES(%s, NOW())' % (constants.sql_tables.his_inputs.name, hks, value)
                            cur.execute(insertstatement)
                        except:
                            pass
                            print(insertstatement)
    
    #                insertstatement = 'INSERT INTO '+constants.sql_tables.his_inputs.name+'(Name, Value, Date) VALUES("' + str(hks) + '",' + str(value) + ', NOW())'
    #                ist = "SELECT NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND table_schema = '%s' AND column_name = '%s'" % (constants.sql_tables.his_inputs.name, datab, hks)
    #                cur.execute(ist)
    #                if not cur.fetchall():
    #                    ist = "ALTER TABLE `%s` ADD `%s` DECIMAL(5,2)" % (constants.sql_tables.his_inputs.name, hks)
    #                    cur.execute(ist)
    
    
                sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last1 = "'+str(ct)+'" WHERE Name = "' + str(device) +'"'
                cur.execute(sql)
                sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET valid = "True" WHERE Name = "' + str(device) +'"'
                cur.execute(sql)
                if not heartbt is None:
                    if hks in validTimers:
                        validTimers[hks].cancel()
                    thread_pt_ = Timer(int(heartbt), invalidTimers, [hks])
                    thread_pt_.start()
                    validTimers[hks] = thread_pt_
                if str(dicti.get("last1")) != "None":
                    sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last2 = "'+str(dicti.get("last1"))+'" WHERE Name = "' + str(device) +'"'
                    cur.execute(sql + sql2)
                if str(hks) != str(device) and add_to_mqtt:
                    data = {"Value":value, "HKS":hks}
                    mqtt_pub("Inputs/" + str(hks), data)
                    mqtt_pub("Inputs/HKS/" + str(hks), data)
        if not filtered:
            sql = 'UPDATE '+constants.sql_tables.inputs.name+' SET last_Value = "'+str(value)+'" WHERE Name = "' + str(device) +'"'
            cur.execute(sql)
    con.close()
#    print('Time spend on inputs: ', str(datetime.datetime.now() - ct))
    return szenen, desc, heartbt

def invalidTimers(hks):
    print('input timed out: ', hks)
    commands = {'Valid': 'False'}
    mdb_set_table(constants.sql_tables.inputs.name, hks, commands, primary='HKS')
