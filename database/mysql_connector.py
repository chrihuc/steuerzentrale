#!/usr/bin/env python

import pandas as pd

import constants

import MySQLdb as mdb
from influxdb import InfluxDBClient
import warnings
warnings.filterwarnings('ignore', category=mdb.Warning)
from threading import Timer
import time
from time import localtime, strftime
import datetime
from outputs.mqtt_publish import mqtt_pub
import copy
from tools import toolbox
import json

from flask import Flask, Markup, request, url_for, render_template, redirect
from flask_table import Table, Col, LinkCol

from flask_wtf import FlaskForm
from wtforms import StringField
import os

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# den Inputs table als Dict abbilden, ID ist der Key, die Reihe dann der Val
# jede Reihe ist ein dictionary
inputs_table = {}

class MyForm(FlaskForm):
    Name = StringField('Name')
    HKS  = StringField('HKS')

#class ItemTable(Table):
#    Name = Col('Name')
#    HKS = Col('HKS')
#    last_Value = Col('last_Value')
#    time = Col('time')


class SortableTable(Table):
    Id = Col('ID')
    Name = Col('Name')
    HKS = Col('HKS')
    last_Value = Col('last_Value')
    time = Col('time')
#    heartbeat
#    latching = Col('latching')
    latched= Col('latched')
#    persistance= Col('persistance')
    link = LinkCol(
        'Link', 'flask_link', url_kwargs=dict(Id='Id'), allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    sort = request.args.get('sort', 'Id')
    filt = request.args.get('filter', '')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(InputsDB.get_sorted_by(sort, reverse, filt),
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()


@app.route('/item/<int:Id>', methods=['GET', 'POST'])
def flask_link(Id):
    error = ""
    element = InputsDB.get_element_by_id(Id)
    form = MyForm()
#    form_action = url_for('index')
    if request.method == 'GET':
        form.Name.data = element.Name
        form.HKS.data = element.HKS
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        print(form.Name.data)
        return 'thank_you'

    # Render the sign-up page
    return render_template('input_el_template.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

#@app.route('/item/<int:Id>')
#def flask_link(Id):
#    element = InputsDB.get_element_by_id(Id)
#    return '<h1>{}</h1><p>{}</p><hr><small>Id: {}</small>'.format(
#        element.Name, element.HKS, element.Id)


class InputsDB(object):
    elements = []
    lock     = False
    """ a little fake database """
    def __init__(self, element):#, Id, name, description):
        self.Id = element['Id']
        self.Name = element['Name']
        self.HKS = element['HKS']
        self.last_Value = element['last_Value']
        self.time = element['time']
        self.heartbeat = None
        if 'heartbeat' in element: self.heartbeat = element['heartbeat']
        self.latching = None
        if 'latching' in element: self.latching = element['latching']
        self.latched = None
        if 'latched' in element: self.latched = element['latched']
        self.persistance = None
        if 'persistance' in element: self.persistance = element['persistance']
        
        self.dict = element
        while InputsDB.lock:
            time.sleep(0.01)
        InputsDB.elements.append(self)

    @classmethod
    def get_elements(cls):
        return cls.elements

    @classmethod
    def build(cls):
        return [InputsDB(item) for key, item in inputs_table.items()]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False, filt='', filtkey='Name'):
        elements = [element for element in cls.get_elements() if filt in element.Name]
        return sorted(
            elements,
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, Id):
        cls.lock = True
        results = [i for i in cls.elements if i.Id == Id]
        cls.lock = False
        if len(results) > 0:
            return results[0]
        return False
    
    @classmethod
    def get_elements_by_name(cls, Name):
        cls.lock = True
        results = [i for i in cls.elements if i.Name == Name]
        cls.lock = False
        return results  
    
    @classmethod
    def get_as_list(cls):
        liste = []
        for element in cls.elements:
            item = {}
            item['Id'] = element.Id
            item['Name'] = element.Name
            item['HKS'] = element.HKS
            item['last_Value'] = element.last_Value
            item['time'] = element.time
            item['heartbeat'] = element.heartbeat
            item['latching'] = element.latching
            item['latched'] = element.latched
            item['persistance'] = element.persistance
            liste.append(item)
        return liste    

#@app.route("/")
#def hello():
#    items = [dict(name='Name1', description='Description1'),
#    dict(name='Name2', description='Description2'),
#    dict(name='Name3', description='Description3')]
#    items = [item for key, item in inputs_table.items()]
#    for item in items:
#        item['name'] = item['Name']
#        item['name'] = item['Name']
    
#    table = ItemTable(items)
    
#    return table.__html__()

# TODO: reconnect of MQTT

#client = mqtt.Client(constants.name + '_mysql_con')
#client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
#client.connect(constants.mqtt_.server)
#client.loop_start()
datab = constants.sql_.DB

validTimers = {}
locklist = {}
persTimers = {}

inputs_dict = {}
prozessspiegel = {}





def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return 'not json serializable' #TypeError ("Type %s not serializable" % type(obj))


def invalidTimers(hks, desc):
    print('input timed out: ', desc)
    commands = {'valid': 'False'}
    mdb_set_table(constants.sql_tables.inputs.name, hks, commands, primary='HKS')
    if validTimers[hks]['fallback']:
        inputs(validTimers[hks]['device'], validTimers[hks]['fallback'], fallingback=True)
#    validTimers.remove(hks)
    validTimers.pop(hks, None)
    with open('hrtbt_timer.jsn', 'w') as fout:
        json.dump(validTimers, fout, default=json_serial)        
    payload = {'Szene':'InputTimedOut', 'desc':'input timed out: '+ desc}
    toolbox.communication.send_message(payload, typ='ExecSzene')          


try:
    with open('hrtbt_timer.jsn') as f:
        full = f.read()            
    alte = json.loads(full)
#    print(alte)
    for key, eintrag in alte.items():
        try:
    #        print(eintrag)
            due = datetime.datetime.strptime(eintrag['due'], '%Y-%m-%dT%H:%M:%S.%f')
            ct = datetime.datetime.now()
            if True: #due > ct:
                delay = (due - ct).seconds + 1
                hks = eintrag['hks']
                desc = eintrag['desc']
                device = eintrag['device']
                fallback = eintrag['fallback']
                entry = {'hks' : hks, 'desc' : desc, 'device':device,'fallback':fallback, 'due':due}
                if delay < 0:
                    invalidTimers(hks, desc)
                else:
                    thread_pt_ = Timer(delay, invalidTimers, [hks, desc])
                    thread_pt_.start()
                    entry['timer'] = thread_pt_
                    validTimers[hks] = entry 
        except Exception as e:
            print(eintrag)
#            self.add_timer(parent, delay, child, exact, retrig, device, start=True)
    print('Heartbeats geladen')
except Exception as e:
    print(str(e))
    try:
        with open('hrtbt_timer.jsn') as f:
            full = f.read()            
        alte = json.loads(full)
        print(alte)     
    except:
        pass
    print('Laden der Heartbeats fehlgeschlagen')
    toolbox.log('Laden der Heartbeats fehlgeschlagen', level=1)

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
        except Exception as e:
            print(e)
            return inpt
    elif "sett" in str(inpt):
        lst = eval(str(inpt))
        if lst[0] == "sett":
            value = setting_r(lst[1])
            try:
                return float(value)
            except Exception as e:
                print(e)
                return value
        else:
            for num, sub in enumerate(lst):
                if "sett" in str(sub):
                    lst[num] = re_calc(sub)
            return lst
    elif "internal" in str(inpt):
        lst = eval(str(inpt))
        if lst[0] == "internal":
            if lst[1] == 'BDQs':
                value = mdb_read_bdqs()
                if value:
                    text = 'BDQs: '+' '.join(value) 
#                    print(text)
                    return text   
                else:
                    return False            
        else:
            for num, sub in enumerate(lst):
                if "sett" in str(sub):
                    lst[num] = re_calc(sub)
            return lst
    else:
        return inpt

def writeInfluxDb(hks, value, utc):
    try:
        if float(value) == 0:
             json_body = [{"measurement": hks,
                          "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                          "fields": {"value": 0.}}] 
        else:      
            json_body = [{"measurement": hks,
                          "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                          "fields": {"value": float(value)}}]
        client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
        client.write_points(json_body)
    except:
        pass
#        print(hks, value, utc)
    return True  

def writeInfluxString(key, value, utc):
    try:
        json_body = [{"measurement": key,
                      "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                      "fields": {"value": str(value)}}]
        client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
        client.write_points(json_body)
    except:
        pass
#        print(key, value, utc)
    return True 

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
    utc = datetime.datetime.utcnow()
    if wert in ('Ein','ein','an'):
        wert = True
    if wert in ('Aus','aus'):
        wert = False
    if 'Inputs.' in setting:
        try:
#            inputs(setting, float(wert))
#            wert = re_calc(wert)
            payload = {'Name':setting,'Value':wert}
        #    on server:
#            toolbox.log(Name, Value, level=9)
#            print(payload)
            toolbox.communication.send_message(payload, typ='InputValue')            
        except:
            print('could not set input', setting, wert)
    else:
        data = {'Value':wert, 'Setting':setting}
        prozessspiegel[setting] = wert
        mqtt_pub("Settings/" + setting, data)
        thread_inflx = Timer(0, writeInfluxString, [setting, wert, utc])
        thread_inflx.start()
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
    if setting in prozessspiegel and constants.prozessspiegel:
        return prozessspiegel[setting]
    value = get_input_value(setting)
    if value is None:
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        value = 0
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.settings.name+" WHERE Name = '"+setting+"'")
            if cur.fetchone()[0] == 0:
                return None
#                sql = 'INSERT INTO '+constants.sql_tables.settings.name+' (Value, Name) VALUES (0,"'+ str(setting) + '")'
#                value = 0
#                cur.execute(sql)
            else:
                sql = 'SELECT * FROM '+constants.sql_tables.settings.name+' WHERE Name = "' + str(setting) +'"'
                cur.execute(sql)
                results = cur.fetchall()
                for row in results:
#                    fname = row[1]
                    value = row[2]
        con.close()
    return value

def valid_r(inpt):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SELECT valid FROM %s WHERE HKS = "%s"' % (constants.sql_tables.inputs.name, inpt)
        cur.execute(sql)
        results = cur.fetchall()
    con.close()
    if results:
        return results[0][0]
    else:
        return True

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
    dicti.update(inputs_r())
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
    
def get_val_in_szenen(device, szene):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SET SQL_SAFE_UPDATES = 0'
        cur.execute(sql)
        sql = 'SELECT ' + device + ' FROM ' +constants.sql_.DB+'.'+constants.sql_tables.szenen.name+' WHERE Name = "' + str(szene) + '"'
#        SELECT V00WOH1RUM1TV01 FROM `set_Szenen` where Name = "Value"
        cur.execute(sql)
        results = cur.fetchall()
    con.close()    
    return results[0][0]

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
            liste.append(copy.copy(dicti))
    con.close()
    return liste

def mdb_read_table_column_filt(db, column, filt='', amount=1000, order="desc", exact=False, filt_on='Name'):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    if type(column) == list:
        column, columns  = '', column
        for col in columns[0:-1]:
            column = column + col + ', '
        column = column + columns[-1]        
    with con:
        cur = con.cursor()
        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
        if exact:
            sql = 'SELECT '+column+' FROM ' + db + ' WHERE ' + filt_on + ' LIKE "' + filt + '" ORDER BY ID ' + order + ' LIMIT ' + str(amount) # % (column,db,filt,order, str(amount))
        else:
            sql = 'SELECT '+column+' FROM ' + db + ' WHERE ' + filt_on + ' LIKE "%' + filt + '%" ORDER BY ID ' + order + ' LIMIT ' + str(amount)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            if type(row[0]) == datetime.datetime:
                rlist.append((int(row[0].strftime("%s"))))
            else:
                rlist.append(eval(str(row[0])))
    con.close()
    return rlist

def mdb_read_table_column_filt2(db, column, filt='', amount=1000, order="desc", exact=False, filt_on='Name'):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = {}
    liste = []    
    if type(column) == list:
        column, columns  = '', column
        for col in columns[0:-1]:
            column = column + col + ', '
        column = column + columns[-1]        
    with con:
        cur = con.cursor()
        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
        if exact:
            sql = 'SELECT '+column+' FROM ' + db + ' WHERE ' + filt_on + ' LIKE "' + filt + '" ORDER BY ID ' + order + ' LIMIT ' + str(amount) # % (column,db,filt,order, str(amount))
        else:
            sql = 'SELECT '+column+' FROM ' + db + ' WHERE ' + filt_on + ' LIKE "%' + filt + '%" ORDER BY ID ' + order + ' LIMIT ' + str(amount)
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]
            liste.append(copy.copy(dicti))
    con.close()
    return liste

def mdb_read_bdqs(amount=1000, order="desc"):
    db = constants.sql_tables.inputs.name
    column = 'description'
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
        sql = 'SELECT %s FROM %s WHERE valid LIKE "False" ORDER BY ID %s LIMIT %s' % (column, db, order, amount)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            rlist.append(row[0])
#            if type(row[0]) == datetime.datetime:
#                rlist.append((int(row[0].strftime("%s"))))
#            else:
#                rlist.append(eval(str(row[0])))
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

def read_inputs_to_inputs_table():
    global inputs_table
    liste = mdb_get_table(constants.sql_tables.inputs.name)
    inputs_table = {}
    for line in liste:
        inputs_table[line['Id']] = line
    print("table loaded")
    InputsDB.build()
#    print(inputs_table)

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

def sendSql(sql):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    cur = con.cursor()
    retrycount = 3
    counter = 1
    while counter <= retrycount:
        try:
#            print(sql)
            cur.execute("SELECT "+datab)
            cur.execute(sql)
            print("success")
            counter = retrycount + 1
        except:
            time.sleep(1)
            counter += 1
            if counter == 4:
                print('could not write to DB')
    con.close()

def writeToCursor(cursor, sql):
#    print(sql)
    retrycount = 10
    counter = 1
    success = False
    while counter <= retrycount and not success:
        try:
            cursor.execute(sql)
            success = True
#            counter = retrycount + 1
        except:
            time.sleep(.15)
            counter += 1
            if counter > 8:
                print('could not write to DB', sql)
    if "8613" in sql:
        print(sql, counter)

def read_inputs_dict():
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dvce_keys = ['HKS', 'Description', 'Setting', 'Logging', 'Id', 'Name', 'Filter', 'debounce', 'heartbeat', 'valid', 'last_value', 'fallback', 'RecoverSzn', 'Kompression']
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM "+datab+"."+constants.sql_tables.inputs.name)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]
            if dicti['Name'] in inputs_dict:
                szn_dict = {key:value for key,value in dicti.items() if key not in dvce_keys}
                inputs_dict[dicti['Name']]['actions'].append(szn_dict)                
            else:
                device_dict = {key:value for key,value in dicti.items() if key in dvce_keys}
                szn_dict = {key:value for key,value in dicti.items() if key not in dvce_keys}
                device_dict['actions'] = [szn_dict]
                inputs_dict[dicti['Name']] = device_dict
    con.close()
    return inputs_dict

# latching (user setting)
# latched (from evaluation automatic) only latch after scene was found
# persistance (user setting)
# violation time (from evaluation automatic)
# funktioniert bei einem Deadband vieillicht nicht, wert muss neu ankommen..
# sollte über interne kommunikation mit ExecSzene' möglich sein.
    
# im ersten schritt nur noch vom Dict lesen und auf SQL und Dict schreiben
def inputs(device, value, add_to_mqtt=True, fallingback=False, persTimer=False):
#    i = 0
    global inputs_table
    ct = datetime.datetime.now()
    utc = datetime.datetime.utcnow()
#    if 'inputs' in device:
#        print(value,device)
    try:
        last_time = locklist[device]
    except KeyError:
        last_time = None
        locklist[device] = ct  
    try:
        value = float(value)
    except Exception as e:
        try:
            value = float(value['value'])
        except Exception as e:
#            print(value)
#            print(device)
            return [], [], None, []
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    
    dicti_1 = {}
    alle_szenen = []
    alle_payloads = []
    descriptions = []
    desc = None
    heartbt = None
    filtered = False
    writeToInflx = False
    hks = device
    
#    print(device,value)
#    if 'MQTT' in device:
#        add_to_mqtt = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"'")
#        if not device in [item['Name'] for key, item in inputs_table.items()]:
        if len(InputsDB.get_elements_by_name(device)) == 0:
#            ids = [int(key) for key in inputs_table.keys()]
#            ids.sort()
#            new_id = ids[-1] + 10
            new_id = InputsDB.get_sorted_by('Id', True)[0].Id + 10
            # stimmt nicht, muss id sein nicht device, wie verändern, damit ich weiterhin iteraten kann?
#            inputs_table[new_id] = {'Name'       :device
            newItem              = {'Name'       :device
                                   ,'HKS'        :device
                                   ,'Description':device
                                   ,'last_Value' :value
                                   ,'time'       :ct
                                   ,'Logging'    :True
                                   ,'Doppelklick':True
                                   ,'Id'         : new_id
                                   }
            InputsDB(newItem)
            print('new Item with id: ', str(new_id))
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
            # wenn wir dann interne sachen nehmen:
#            inputs_table_c = copy.copy(inputs_table)                    
#            results2 = [item for key, item in inputs_table_c.items() if item['Name'] == device]
            #dicti_2 = results2[device]
            last_value = dicti_1['last_Value']            
            # Filtern, wenn groesser oder kleiner Messung ignorieren
            filtering = dicti_1['Filter']
            hks = dicti_1['HKS']
            # könnte fallingback auch vorher definieren
            if fallingback and dicti_1['fallback'] is not None:
                value = float(dicti_1['fallback'])
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
                valid = dicti_1['valid']
                heartbt = dicti_1['heartbeat']
                desc = dicti_1['Description']
                komp = dicti_1['Kompression']
                hyst = dicti_1['Hysterese']
                recSzn = dicti_1['RecoverSzn']
                offset = dicti_1['offset']
                if str(offset) != 'None':
                    offset = float(offset)
                    value = float(value) + offset
                if heartbt and str(valid) == "False" and not fallingback:
                    payload = {'Szene':'InputTimedOut', 'desc':'input recovered: '+ desc}
                    toolbox.communication.send_message(payload, typ='ExecSzene')
                    if recSzn:
                        payload = {'Szene':recSzn}
                        toolbox.communication.send_message(payload, typ='ExecSzene')                                    
                if last_value is None: 
                    last_value = value
                    writeToInflx = True
                elif float(last_value) != float(value):
                    writeToInflx = True
                if str(komp) in ['None', 'False']:
                    writeToInflx = True
                if str(komp) in ['Bool']:
                    if (float(last_value) <= 0.0 and float(value) >= 0.0) or (float(last_value) >= 0.0 and float(value) <= 0.0):
                        writeToInflx = True   
                    else:
                        writeToInflx = False
                if not last_time:
                    try:
                        last_time = dicti_1['last1']
                    except:
                        last_time = ct - datetime.timedelta(hours=1)
                debounce = dicti_1['debounce']
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
                gradient = 0
                if deltaTm > 0:
                    try:
                        deltaX = float(value) - float(last_value)
                        gradient = deltaX #/ deltaTm
                    except:
                        print(value, last_value, device)
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

                for row in results:
                    szenen = []
                    latchMerker = False
                    payloads = []
                    kondition = []
                    
                    violTime = None
                    latched = None                    
                    
                    single = True
                    dicti = {}
                    for i in range (0,len(row)):
                        dicti[field_names[i]] = row[i]
                        
                    descri = dicti.get("Status")
                    if descri is None:
                        descri = ''                        
                        
                    doppelklick = dicti.get("Doppelklick")
                    if ct >= db_time:
                        # Hysteres einberechnen
                        lt = None
                        if dicti['Value_lt'] is not None:
                            lt = float(re_calc(dicti['Value_lt']))
                            if hyst is not None and str(dicti.get('latching')) == "True" and str(dicti.get('latched')) == "True":
                                lt = lt + float(hyst)
                        gt = None
#                        print('value_gt', dicti['Value_gt'])
                        if dicti['Value_gt'] is not None:
                            gt = float(re_calc(dicti['Value_gt']))
#                            print('value_gt', gt)
                            if hyst is not None and str(dicti.get('latching')) == "True" and str(dicti.get('latched')) == "True":
                                gt = gt - float(hyst)                             
#                        print('value_gt_1', gt)        
                        append = True
                        if (lt is not None and lt <= float(value)):
                            append = False
                        if (dicti['Value_eq'] is not None and float(re_calc(dicti['Value_eq'])) != float(value)):
                            append = False
#                        print('value_gt_1', gt)                             
                        if (gt is not None and gt >= float(value)):
                            append = False
#                        print('append', append)
                        # Gradient
                        if (dicti['Gradient_lt'] is not None and float(re_calc(dicti['Gradient_lt'])) <= gradient):
                            append = False
#                        if (dicti['Gradient_eq'] is not None and float(re_calc(dicti['Gradient_eq'])) != gradient):
#                            append = False
                        if (dicti['Gradient_gt'] is not None and float(re_calc(dicti['Gradient_gt'])) >= gradient):
                            append = False
                        if append and persTimer and dicti.get('violTime') is None: 
                            # Bedingungen sind erfüllt aber die Funktion wurde getimed ausgelöst, Peristtime, aber in der Zwischenzeit wurde schon resettiert
                            append = False
                        if str(dicti.get("last2")) != "None" and append:
                            if ct - dicti.get("last2") < datetime.timedelta(hours=0, minutes=0, seconds=4):
                                if dicti.get("Dreifach") is not None:
                                    szenen.append(dicti.get("Dreifach"))
                                    payloads.append(dicti.get("Payload"))
                                    kondition.append(desc + " " + descri)
                                    single = False
                            elif ct - dicti.get("last1") < datetime.timedelta(hours=0, minutes=0, seconds=3):
                                if dicti.get("Doppel") is not None:                                
                                    szenen.append(dicti.get("Doppel"))
                                    payloads.append(dicti.get("Payload"))
                                    kondition.append(desc + " " + descri)
                                    single = False
                        if str(doppelklick) != "True": single = True                            
                        if single and append and dicti.get(setting_r("Status")) is not None: 
                            szenen.append(dicti.get(setting_r("Status")))
                            payloads.append(dicti.get("Payload"))
                            kondition.append(desc + " " + descri)
                        if append and dicti.get('Immer') is not None:
                            szenen.append(dicti.get('Immer'))
                            payloads.append(dicti.get("Payload"))
                            kondition.append(desc + " " + descri)
                        #if append and dicti.get('violTime') is None: # bedinung ist erfüllt und ViolTime war nicht gesetzt (set)
                        if append and (dicti.get('violTime') is None or dicti.get('persistance') is None): # bedinung ist erfüllt und ViolTime war nicht gesetzt (set)
                            violTime = str(ct)
                            # hier können wir dann den timer starten, oder besser dort wo wir auch wissen, das pesistence gibt
                        if not append and not dicti.get('violTime') is None: # bedingung nicht erfüllt und ViolTime war gesetzt (reset)
                            violTime = 'NULL'
                        if append:
                            latchMerker = True
                        if append and dicti.get('persistance') is not None:  # wir hätten was auszufühern aber persistence ist grösser null
                            if dicti.get('violTime') is not None:  # Zeit der ersten Bedinungsverletzung ist eingetragen
                                if ct - dicti.get("violTime") < datetime.timedelta(seconds=dicti.get('persistance')): # persistence zeit ist noch nicht abgelaufen
                                    szenen = []
                                    payloads = []
                                    kondition = []
                                    latchMerker = False
                            if dicti.get('violTime') is None and datetime.timedelta(seconds=dicti.get('persistance')) > datetime.timedelta(seconds=0):
                                # bedingung wurde jetzt gerade erfüllt, aber wir müssen persistence abwarten
                                szenen = []
                                payloads = []
                                kondition = []
                                latchMerker = False
                                # wir starten einen timer um zu schauen ob der Wert sich in der Persistence Zeit nicht erholt hat:
                                if not persTimer:
                                    thread_persis = Timer(int(dicti.get('persistance')), inputs, [device, value, False, False, True])
                                    thread_persis.start()                                
                        if str(dicti.get('latching')) == "True":
                            if not latchMerker and str(dicti.get('latched')) == "True":
                                latched = 'False'
                                # anti szene (praktisch das reset):
                                if dicti.get('ResetSzene') is not None:
                                    szenen.append(dicti.get('ResetSzene'))
                                    payloads.append(dicti.get("Payload"))
                                    kondition.append(desc + " " + descri)
                            elif latchMerker and str(dicti.get('latched')) == "True":
                                szenen = []
                                payloads = []
                                kondition = []
                            elif latchMerker and str(dicti.get('latched')) != "True": 
#                                print(szenen)
                                latched = 'True'
#                        print(lt,gt,latched)
                        # falls bedinungen erfüllt die Zeiten anpassen:
                        lasttimes = ""
                        # debug
                        if append:
                            inputs_table[dicti['Id']]['last1'] = ct
                            if str(dicti.get("last1")) != "None":
                                lasttimes = ', last2 = "%s", last1 = "%s"' % (dicti.get("last1"), ct)
                                inputs_table[dicti['Id']]['last2'] = dicti.get("last1")
                            else:
                                lasttimes = ', last1 = "%s"' % (ct)
#                        if device == 'Wetter/RegenWarnung':
#                            print(value)
#                            print('UPDATE %s SET violTime = "%s"%s, latched = "%s" WHERE Id = "%s"' % (constants.sql_tables.inputs.name, violTime, lasttimes, latched, dicti.get('Id')))
#                            print(violTime is not None and latched is not None)                                
                        if violTime is not None and latched is not None: # 
                            sql = 'UPDATE %s SET violTime = "%s"%s, latched = "%s" WHERE Id = "%s"' % (constants.sql_tables.inputs.name, violTime, lasttimes, latched, dicti.get('Id'))
                            writeToCursor(cur, sql)
         # ACHTUNG musste wie die nächste Zeile sein:                   
                            #inputs_table[dicti['Id']]['violTime'] = violTime
#                            results2[0][dicti['Id']]['violTime'] = violTime
#                            cur.execute(sql)
                        elif violTime is not None and latched is None:  
                            sql = 'UPDATE %s SET violTime = "%s"%s WHERE Id = "%s"' % (constants.sql_tables.inputs.name, violTime, lasttimes, dicti.get('Id'))
                            writeToCursor(cur, sql)
#                            cur.execute(sql)   
                        elif violTime is None and latched is not None:
                            sql = 'UPDATE %s SET latched = "%s"%s WHERE Id = "%s"' % (constants.sql_tables.inputs.name, latched, lasttimes, dicti.get('Id'))
                            writeToCursor(cur, sql)                            
#                            cur.execute(sql) 
                    alle_szenen += szenen       
                    alle_payloads += payloads
                    descriptions += kondition                     
    #            get stting and logging
                # deprecated
#                writeToCursor(cur, "SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Setting = 'True'")
#                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Setting = 'True'")
#                if cur.fetchone()[0] > 0:
#                    setting_s(hks, value)
                writeToCursor(cur,"SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Logging = 'True'")
#                cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"' AND Logging = 'True'")
                if cur.fetchone()[0] > 0 and str(hks) != str(device) and writeToInflx and not persTimer:
#                    try:
#                        insertstatement = 'INSERT INTO %s (%s, Date) VALUES(%s, NOW())' % (constants.sql_tables.his_inputs.name, hks, value)
#                        cur.execute(insertstatement)
#                    except:
#                        try:
#                            ist = "ALTER TABLE `%s` ADD `%s` DECIMAL(8,3)" % (constants.sql_tables.his_inputs.name, hks)
#                            cur.execute(ist)
#                            insertstatement = 'INSERT INTO %s (%s, Date) VALUES(%s, NOW())' % (constants.sql_tables.his_inputs.name, hks, value)
#                            cur.execute(insertstatement)
#                        except:
#                            pass
                    thread_inflx = Timer(0, writeInfluxDb, [hks, value, utc])
                    thread_inflx.start()
#                            print(insertstatement)
    
    #                insertstatement = 'INSERT INTO '+constants.sql_tables.his_inputs.name+'(Name, Value, Date) VALUES("' + str(hks) + '",' + str(value) + ', NOW())'
    #                ist = "SELECT NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND table_schema = '%s' AND column_name = '%s'" % (constants.sql_tables.his_inputs.name, datab, hks)
    #                cur.execute(ist)
    #                if not cur.fetchall():
    #                    ist = "ALTER TABLE `%s` ADD `%s` DECIMAL(5,2)" % (constants.sql_tables.his_inputs.name, hks)
    #                    cur.execute(ist)
    
    
                if str(hks) != str(device) and add_to_mqtt:
                    data = {"Value":value, "HKS":hks}
                    mqtt_pub("Inputs/" + str(hks), data)
                    mqtt_pub("Inputs/HKS/" + str(hks), data)
        if not filtered and not persTimer:
            sql = 'UPDATE %s SET valid = "%s", last_Value = "%s", time = "%s" WHERE Name = "%s" AND (enabled = "True" OR enabled is NULL)' % (constants.sql_tables.inputs.name, not fallingback, value, ct, device)
#            thread_sql = Timer(1, sendSql, [sql])
            retrycount = 3
            counter = 1
            while counter <= retrycount:
                try:
                    cur.execute(sql)
                    counter = retrycount + 1
                except:
                    time.sleep(.1)
                    counter += 1
                    if counter == 4:
                        print('could not write to DB')            
#            thread_sql.start()
            prozessspiegel[hks] = value
#            results2 = [item for key, item in inputs_table_c.items() if item['Name'] == device]
            results2 = InputsDB.get_elements_by_name(device)
            for item in results2:
                item.last_Value = value
                item.time       = ct
        if heartbt and not fallingback and not persTimer:
            if hks in validTimers:
                validTimers[hks]['timer'].cancel()
            entry = {'hks' : hks, 'desc' : desc, 'device':device, 'fallback':dicti_1['fallback']}
            entry['due'] = datetime.datetime.now() + datetime.timedelta(0,int(heartbt))
            thread_pt_ = Timer(int(heartbt), invalidTimers, [hks, desc])
            thread_pt_.start()
            entry['timer'] = thread_pt_
            validTimers[hks] = entry
            with open('hrtbt_timer.jsn', 'w') as fout:
                json.dump(validTimers, fout, default=json_serial)            
#            print(validTimers.keys())
    con.close()
#    print('Time spend on inputs: ', str(datetime.datetime.now() - ct))
    if persTimer:
        for idx, szene in enumerate(alle_szenen):
            payload = {'Szene':szene, 'desc':descriptions[idx]}
            toolbox.communication.send_message(payload, typ='ExecSzene')
    return alle_szenen, descriptions, heartbt, alle_payloads


read_inputs_to_inputs_table()

def apptask():
    app.run(host='0.0.0.0', port=4444)
    
def main(): 
    apptimer = Timer(0, apptask)
    apptimer.start()     
    while constants.run:
        time.sleep(1)
    
    with open('inputs_table.jsn', 'w') as fout:
        json.dump(InputsDB.get_as_list(), fout, default=json_serial) 
    print("table written")
