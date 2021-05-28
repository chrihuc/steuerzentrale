#!/usr/bin/env python

import pandas as pd
import glob

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

from multiprocessing import Process

from flask import Flask, Markup, request, url_for, render_template, redirect
from flask_table import Table, Col, LinkCol, ButtonCol

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
import os

from database.intern_db import DatabaseIntern, convert_to, DatabaseSzenen

properties_iptDB = { 'Id':          (None, int)
                    ,'Name':        ('HKS', str)
                    ,'HKS':         ('HKS', str)
                    ,'Value':       (0, float)
                    ,'time':        (None, datetime.datetime)
                    ,'Description': (None, str)
                    ,'Status' :     (None, str)
                    ,'Logging' :    (True, bool)
                    ,'Doppelklick' :(False, bool)
                    ,'last1' :      (None, datetime.datetime)
                    ,'last2' :      (None, datetime.datetime)
                    ,'Filter' :     (None, str)
                    ,'offset' :     (None, float)
                    ,'debounce' :   (None, int)
                    ,'heartbeat' :  (None, int)
                    ,'latching' :   (None, bool)
                    ,'latched' :    (None, bool)
                    ,'latch_always':(False, bool)
                    ,'persistance' :(None, int)
                    ,'violTime' :   (None, datetime.datetime)
                    ,'valid' :      (True, bool)
                    ,'lastChange':  (None, datetime.datetime)
                    ,'frozen':      (None, int)
                    ,'enabled' :    (True, bool)
                    ,'fallback':    (None, float)
                    ,'RecoverSzn':  (None, str)
                    ,'Value_lt':    (None, str)
                    ,'Value_eq':    (None, str)
                    ,'Value_gt':    (None, str)
                    ,'Hysterese':   (None, float)
                    ,'Kompression': (None, str)
                    
                    ,'Immer':       (None, str)
                    ,'ResetSzene':  (None, str)
                    ,'Wach':        (None, str)
                    ,'Wecken':      (None, str)
                    ,'Schlafen':    (None, str)
                    ,'Schlummern':  (None, str)
                    ,'Leise':       (None, str)
                    ,'AmGehen':     (None, str)
                    ,'Gegangen':    (None, str)
                    ,'Abwesend':    (None, str)
                    ,'Urlaub':      (None, str)
                    ,'Besuch':      (None, str)
                    ,'Doppel':      (None, str)
                    ,'Dreifach':    (None, str)
                    ,'Sturm_anz':   (None, int)
                    ,'Sturm_dauer': (None, int)
                    ,'Sturm':       (None, str)
                    ,'Sturm_count': (0, int)
                    ,'Alarm':       (None, str)
                    ,'Payload':     (None, str)
                    
                    ,'debug':       (False, bool)
                    }


device_props =[ 'HKS'
               ,'Description'
               ,'Logging'
               ,'Filter'
               ,'offset'
               ,'debounce'
               ,'heartbeat'
               ,'valid'
               ,'Kompression'
               ,'fallback'
               ,'Sturm_anz', 'Sturm_dauer', 'Sturm', 'Sturm_count'
               ,'lastChange', 'frozen'
               ]

properties_sznDB = { 'Id':              (None, int)
                    ,'Name':            (None, str)
                    ,'Prio':            (None, int)
                    ,'MQTTChannel':     (None, str)
                    ,'Beschreibung':    (None, str)
                    ,'Durchsage':       (None, str)
                    ,'Karenz':          (None, str)
                    ,'Latching':        (None, str)
                    ,'Gruppe':          (None, str)
#                    ,'inApp':           (None, str)
                    ,'Setting':         (None, str)
                    ,'Delay':           (None, str)
                    ,'Follows':         (None, str)
                    ,'Cancels':         (None, str)
                    ,'Bedingung':       (None, str)
                    ,'AutoMode':        (None, str) 
                    ,'intCmd':          (None, str)  
                    ,'LastUsed':        (None, datetime.datetime)
                    ,'Enabled':         (None, str)

                    ,'A00EIN1ADV1ST01':         (None, str)
                    ,'A00EIN1GEN1LI01':         (None, str)
                    ,'A00GAR1POW1DO01':         (None, str)
                    ,'A00GAR1WAS1DO01':         (None, str)
                    ,'A00GAR1WAS3DO01':         (None, str)
                    ,'A00GAR1WAS2DO01':         (None, str)
                    ,'A00RAS1MAE1DO01':         (None, str)
                    ,'A00TER1ADV1ST01':         (None, str)
                    ,'A00TER1DEK1LI01':         (None, str)
                    ,'A00TER1DEK1DO01':         (None, str)
                    ,'A00TER1GEN1LI01':         (None, str)
                    ,'A00TER1GEN1PO01':         (None, str)
                    ,'A00TER1GEN1ST01':         (None, str)
                    ,'A00TER2MAR1DO01':         (None, str) # button fernbedienung
                    ,'A00TER2MAR1DO02':         (None, str) # button fernbedienung
                    ,'A00TER2MAR1DO03':         (None, str) # button fernbedienung
                    ,'A00TER2MAR1DO99':         (None, str) # Fernbedienung programmieren (button 1 und 2)  
                    ,'A00TER2MAR1PO01':         (None, str) # Strom Markise (Shelly)
                    ,'V00ESS1DEK1LI01':         (None, str)
                    ,'V00ESS1TUR1SR01':         (None, str) # Store
                    ,'V00ESS1RUM1LI01':         (None, str)
                    ,'V00ESS1OUT1PO01':         (None, str)
                    ,'V00FLU1DEK1LI01':         (None, str)
                    ,'V00FLU1SRA1LI01':         (None, str)
                    ,'V00FLU1TUE1DO03':         (None, str)
                    ,'V00FLU1TUE1DO03conf':     (None, str)
                    ,'V00FLU1TUE1PC01':         (None, str)
                    ,'V00KUE1ZIM1PO01':         (None, str)
                    ,'V00KUE1ADV1LI01':         (None, str)
                    ,'V00KUE1DEK1LI01':         (None, str)
                    ,'V00KUE1DEK1LI02':         (None, str)
                    ,'V00KUE1FEN1SR01':         (None, str) # Store                    
                    ,'V00KUE1RUM1AV11':         (None, str)
                    ,'V00KUE1RUM1LI01':         (None, str)
                    ,'V00KUE1RUM1ST01':         (None, str)
                    ,'V00KUE1RUM1TE01':         (None, str)
                    ,'V00KUE1SRA1LI01':         (None, str)
                    ,'V00TOI1DEK1LI01':         (None, str)
                    ,'V00TRE1RUM1AL01':         (None, str)
                    ,'V00TRE1RUM1AL02':         (None, str)
                    ,'V00TRE1RUM1AL03':         (None, str)
                    ,'V00TRE1RUM1LI01':         (None, str)
                    ,'V00WOH1ADV1LI01':         (None, str)
                    ,'V00WOH1ADV1LI02':         (None, str)
                    ,'V00WOH1DEK1LI01':         (None, str)
                    ,'V00WOH1FEN1SR01':         (None, str) # Store fenster klein
                    ,'V00WOH1RUM1AV01':         (None, str)
                    ,'V00WOH1RUM1AV11':         (None, str)
                    ,'V00WOH1RUM1DI01':         (None, str)
                    ,'V00WOH1RUM1DO10':         (None, str)
                    ,'V00WOH1RUM1LI11':         (None, str)
                    ,'V00WOH1RUM1LI12':         (None, str)
                    ,'V00WOH1RUM1LI13':         (None, str)
                    ,'V00WOH1RUM1LI14':         (None, str)
                    ,'V00WOH1RUM1PC01':         (None, str)
                    ,'V00WOH1RUM1ST01':         (None, str)
                    ,'V00WOH1RUM1ST02':         (None, str)
                    ,'V00WOH1RUM1TV01':         (None, str)
                    ,'V00WOH1SRA1LI01':         (None, str)
                    ,'V00WOH1SRA1LI02':         (None, str)
                    ,'V00WOH1SRA1LI03':         (None, str)
                    ,'V00WOH1SRA1LI04':         (None, str)
                    ,'V00WOH1SRA1LI11':         (None, str)
                    ,'V00WOH1SRA1PC01':         (None, str)
                    ,'V00WOH1STV01':            (None, str)
                    ,'V00WOH1STV02':            (None, str)
                    ,'V00WOH1TUR1LI01':         (None, str)
                    ,'V00WOH1TUR1SR01':         (None, str) # Store Tür
                    ,'V00ZIM0RUM0DO01':         (None, str)
                    ,'V00ZIM0RUM0DO02':         (None, str)
                    ,'V01BAD1DEK1LI01':         (None, str)
                    ,'V01BAD1DEK1LI02':         (None, str)
                    ,'V01BAD1RUM1AV11':         (None, str)
                    ,'V01BAD1RUM1LI02':         (None, str)
                    ,'V01BAD1FEN1SR01':         (None, str) # Store
                    ,'V01BUE1DEK1LI01':         (None, str)
                    ,'V01BUE1FEN1SR01':         (None, str) # Store
                    ,'V01BUE1FEN2SR01':         (None, str) # Store
                    ,'V01BUE1STL1DO01':         (None, str)
                    ,'V01FLU1DEK1LI01':         (None, str)
                    ,'V01KID1DEK1LI01':         (None, str)
                    ,'V01KID1FEN1SR01':         (None, str) # Store
                    ,'V01KID1RUM1AV11':         (None, str)
                    ,'V01KID1RUM1LI02':         (None, str)
                    ,'V01KID1ZIM1ST01':         (None, str)
                    ,'V01KID1ZIM1ST02':         (None, str)
                    ,'V01KID1ZIM1LI01':         (None, str)
                    ,'V01KID1UIM1LI02':         (None, str)                    
                    ,'V01SCH1BET1LI01':         (None, str)
                    ,'V01SCH1BET1LI02':         (None, str)
                    ,'V01SCH1DEK1LI01':         (None, str)
                    ,'V01SCH1FEN1SR01':         (None, str) # Store
                    ,'V01SCH1FEN2SR01':         (None, str) # Store
                    ,'V01SCH1RUM1AV11':         (None, str)
                    ,'V01SCH1RUM1LI02':         (None, str)
                    ,'V01SCH1RUM1LI10':         (None, str)
                    ,'V01SCH1RUM1LI11':         (None, str)
                    ,'V01SCH1RUM1PO01':         (None, str) # Srom Steckdosen
                    ,'V01SCH1STE1LI01':         (None, str)
                    ,'V01SCH1STE1LI02':         (None, str)
                    ,'V02BAD1DEK1LI01':         (None, str)
                    ,'V02TRE1DEK1LI01':         (None, str)
                    ,'V02ZIM1DEK1LI01':         (None, str)
                    ,'V02ZIM1FEN1SR01':         (None, str) # Store
                    ,'V02ZIM1FEN2SR01':         (None, str) # Store                    
                    ,'V02ZIM1RUM1ST01':         (None, str)
                    ,'VIRKOM1SSH1PC01':         (None, str)
                    ,'VIRKOM1SSH1PC02':         (None, str)
                    ,'VIRKOM1SSH1PC03':         (None, str)
                    ,'VIRKOM1SSH1PC04':         (None, str)
                    ,'VIRKOM1SSH1PC05':         (None, str)
                    ,'Vm1FLU1DEK1LI01':         (None, str)
                    ,'Vm1GAR1PAR1LI01':         (None, str)
                    ,'Vm1GAR1TUR1DI01':         (None, str)
                    ,'Vm1ZIM1DEK1LI01':         (None, str)
                    ,'Vm1ZIM1PFL1DO01':         (None, str)
                    ,'Vm1ZIM1PFL1LI01':         (None, str)
                    ,'Vm1ZIM1RUM1AV11':         (None, str)
                    ,'Vm1ZIM1RUM1DO01':         (None, str)
                    ,'Vm1ZIM1RUM1ST01':         (None, str)
                    ,'Vm1ZIM1RUT1PC01':         (None, str)
                    ,'Vm1ZIM1SAT1LI01':         (None, str)
                    ,'Vm1ZIM1SCA1DO01':         (None, str)
                    ,'Vm1ZIM1SEV1PC01':         (None, str)
                    ,'Vm1ZIM1TUR1DO10':         (None, str)
                    ,'Vm1ZIM2DEK1LI01':         (None, str)
                    ,'Vm1ZIM2NAT1DO01':         (None, str)
                    ,'Vm1ZIM2TRO1DO01':         (None, str)
                    ,'Vm1ZIM2WAS1DO01':         (None, str)
                    ,'Vm1ZIM3DEK1LI01':         (None, str)
                    ,'Vm1ZIM3RUM1ST01':         (None, str)
                    ,'Vm1ZIM3STR1DO01':         (None, str)

                    ,'debug':                   (False, bool)                    
                    }

InputsDatabase = DatabaseIntern(properties_iptDB, 'inputs_table.jsn')

SzenenDatabase = DatabaseSzenen(properties_sznDB, 'szenen_table.jsn')

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# den Inputs table als Dict abbilden, ID ist der Key, die Reihe dann der Val
# jede Reihe ist ein dictionary
inputs_table = {}

class TriggerForm(FlaskForm):
    Name = StringField('Name')
    HKS  = StringField('HKS')
    Description  = StringField('Description')
    Status  = StringField('Status')
    Logging  = SelectField('Logging', choices =[(False,False),(True,True)]) 
    Doppelklick  = SelectField('Doppelklick', choices =[(False,False),(True,True)]) 
    last1  = StringField('last1')
    Filter  = StringField('Filter')
    offset  = StringField('offset')
    debounce  = StringField('debounce')
    heartbeat  = StringField('heartbeat')
    frozen     = StringField('frozen')
    latching  = StringField('latching')
    latch_always  = SelectField('latch_always', choices =[(False,False),(True,True)]) 
#    violTime = StringField('violTime')
    persistance  = StringField('persistance')
    Kompression  = SelectField('Kompression', choices =[(False,False),(True,True),('Bool','Bool')]) 
    enabled      = SelectField('enabled', choices =[(False,False),(True,True)]) 
#    Immer          = StringField('Immer')
    Immer          = SelectField(u'Immer', choices = SzenenDatabase.get_all_names())
    Value_lt          = StringField('Value_lt')
    Value_eq          = StringField('Value_eq')
    Value_gt          = StringField('Value_gt') 
    Hysterese          = StringField('Hysterese')
    ResetSzene     = StringField('ResetSzene')
    Wach           = SelectField('Wach') 
    Wecken         = StringField('Wecken') 
    Schlafen       = StringField('Schlafen') 
    Schlummern     = StringField('Schlummern')
    Leise          = StringField('Leise') 
    AmGehen        = StringField('AmGehen') 
    Gegangen       = StringField('Gegangen') 
    Abwesend       = StringField('Abwesend') 
    Urlaub         = StringField('Urlaub') 
    Besuch         = StringField('Besuch') 
    Doppel         = StringField('Doppel') 
    Dreifach       = StringField('Dreifach') 
    Sturm_anz      = StringField('Sturm_anz') 
    Sturm_dauer    = StringField('Sturm_dauer') 
    Sturm          = SelectField('Sturm', choices = SzenenDatabase.get_all_names())
    Alarm          = StringField('Alarm') 
    Payload        = StringField('Payload')     
    debug          = SelectField('debug', choices =[(False,False),(True,True)]) 
    fallback       = StringField('fallback')


class SortableTableInputs(Table):
    Id = Col('ID')
    Name = Col('Name')
#    Name = LinkCol(
#        'Name', 'index_inputs', url_kwargs=dict(Name='Name'), allow_sort=False)
    HKS = Col('HKS')
    Description = Col('Description')
    Status = Col('Status')
    time = Col('time')
    Value = Col('Value')
    lastChange = Col('lastChange')
    Value_lt =  Col('Value_lt')
    Value_eq =  Col('Value_eq')   
    Value_gt =  Col('Value_gt') 
    violTime = Col('violTime')
#    heartbeat
    latching = Col('latching')
    latched= Col('latched')
    latch_always= Col('latch_always')
    persistance= Col('persistance')
    link = LinkCol(
        'Edit', 'flask_link', url_kwargs=dict(Id='Id'), allow_sort=False)
    new = LinkCol(
        'New Trigger', 'new_trig', url_kwargs=dict(Id='Id'))    
    delet = LinkCol(
        'Delete', 'delete_id', url_kwargs=dict(Id='Id'))
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index_inputs', sort=col_key, direction=direction)

class SortableTableSzenen(Table):
#    Id           = Col('Id')
    Id = LinkCol(
        'Id', 'index_szenen', url_kwargs=dict(Id='Id'), allow_sort=False, attr=('Id'))
#    Name         = Col('Name')
    Name = LinkCol(
        'Name', 'index_inputs', url_kwargs=dict(Scene='Name'), allow_sort=False, attr=('Name'))
    Execute      = ButtonCol('Ausführen', 'execScene', url_kwargs=dict(Scene='Name',Id='Id'))
    LastUsed     = Col('LastUsed')
    Prio         = Col('Prio')
    MQTTChannel  = Col('MQTTChannel')
    Beschreibung = Col('Beschreibung')
    Durchsage    = Col('Durchsage')
    Karenz       = Col('Karenz')
    Latching     = Col('Latching')
#    Gruppe       = Col('Gruppe') # Todo linkcol
    Gruppe = LinkCol(
        'Gruppe', 'index_szenen', url_kwargs=dict(Gruppe='Gruppe'), allow_sort=True, attr=('Gruppe'))    
    #inApp        = Col('inApp')
    Setting      = Col('Setting')
    Delay        = Col('Delay')
#    Follows      = Col('Follows') # Todo linkcol
    Follows = LinkCol(
        'Follows', 'index_szenen', url_kwargs=dict(Follows='Name'), allow_sort=True, attr=('Follows'))      
#    Cancels      = Col('Cancels') # Todo linkcol
    Cancels = LinkCol(
        'Cancels', 'index_szenen', url_kwargs=dict(Cancels='Name'), allow_sort=True, attr=('Cancels'))      
    Bedingung    = Col('Bedingung')
    AutoMode     = Col('AutoMode')
    intCmd       = Col('intCmd')
    Enabled      = Col('Enabled')
    editconf = LinkCol(
        'Edit config', 'edit_szn', url_kwargs=dict(Id='Id'), allow_sort=False)
    editug = LinkCol(
        'Edit UG', 'edit_szn_ug', url_kwargs=dict(Id='Id'), allow_sort=False)    
    editeg = LinkCol(
        'Edit EG', 'edit_szn_eg', url_kwargs=dict(Id='Id'), allow_sort=False)    
    editog = LinkCol(
        'Edit OG', 'edit_szn_og', url_kwargs=dict(Id='Id'), allow_sort=False)   
    editdg = LinkCol(
        'Edit DG', 'edit_szn_dg', url_kwargs=dict(Id='Id'), allow_sort=False)   
    edita = LinkCol(
        'Edit Aussen', 'edit_szn_a', url_kwargs=dict(Id='Id'), allow_sort=False)       
    edita = LinkCol(
        'Edit Storen', 'edit_szn_store', url_kwargs=dict(Id='Id'), allow_sort=False)     
    new = LinkCol(
        'Copy Szene', 'copy_szene', url_kwargs=dict(Id='Id')) 
    delet = LinkCol(
        'Delete', 'delete_szene', url_kwargs=dict(Id='Id'))

    allow_sort = True
    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index_szenen', sort=col_key, direction=direction)


for key, value in properties_sznDB.items():
    if any([i in key for i in ['V0', 'Vm', 'A0', 'VIR']]):
        SortableTableSzenen.add_column(key, Col(key))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def read_inputs_to_inputs_table():
#    global inputs_table
    inputs_table = {}
    success = False
    file = 'inputs_table.jsn'
    index = 0
    files = glob.glob("./db_backup/inputs_table*" )
    files.sort()
    index = len(files)
#    print(files)
    # neu
    while not success:
        try:
            with open(file) as f:
                inptsjsn = f.read()            
            inputs_table = json.loads(inptsjsn)
            print("inputs table loaded from file")
            success = True
        except Exception as e:
            print("COULD NOT LOAD INPUTS TABLE")
            print(e)
            index -= 1
            if index >= 0:
                file = files[index]
            else:
                raise Exception('Kein Backup', 'inputs')
    return inputs_table
    
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

def read_szenen_to_inputs_table():
#    global inputs_table
    szenen_table = {}
    success = False
    file = 'szenen_table.jsn'
    index = 0
    files = glob.glob("./db_backup/szenen_table*" )
    files.sort()
    index = len(files)    
    # neu
    while not success:
        try:
            with open(file) as f:
                szenejsn = f.read()            
            szenen_table = json.loads(szenejsn)
            print("Szenen table loaded from file")
            success = True
        except Exception as e:
            print("COULD NOT LOAD SZENEN TABLE")
            print(e)
            index -= 1
            if index >= 0:
                file = files[index]
            else:
                raise Exception('Kein Backup', 'szenen')
    return szenen_table

print('baue')
InputsDatabase.build(read_inputs_to_inputs_table())
SzenenDatabase.build(read_szenen_to_inputs_table())

class SzenenForm(FlaskForm):
    Name         = StringField('Name')
    Prio         = StringField('Prio')
    MQTTChannel  = StringField('MQTTChannel')
    Beschreibung = StringField('Beschreibung')
    Durchsage    = StringField('Durchsage')
    Karenz       = StringField('Karenz')
    Latching     = StringField('Latching')
    Gruppe       = StringField('Gruppe')
    inApp        = StringField('inApp')
    Setting      = StringField('Setting')
    Delay        = StringField('Delay')
    Follows      = StringField('Follows')
    Cancels      = StringField('Cancels')
    Bedingung    = StringField('Bedingung')
    AutoMode     = StringField('AutoMode')
    intCmd       = StringField('intCmd')
    LastUsed     = StringField('LastUsed')
    Enabled      = SelectField('Enabled', choices =[(False,False),(True,True)])
    debug        = SelectField('debug', choices =[(False,False),(True,True)])

class SzenenFormA(FlaskForm):
    A00EIN1ADV1ST01        = StringField(SzenenDatabase.get_description('A00EIN1ADV1ST01')+': '+'A00EIN1ADV1ST01')      
    A00EIN1GEN1LI01        = StringField(SzenenDatabase.get_description('A00EIN1GEN1LI01')+': '+'A00EIN1GEN1LI01')       
    A00GAR1POW1DO01        = StringField(SzenenDatabase.get_description('A00GAR1POW1DO01')+': '+'A00GAR1POW1DO01')       
    A00GAR1WAS1DO01        = StringField(SzenenDatabase.get_description('A00GAR1WAS1DO01')+': '+'A00GAR1WAS1DO01')       
    A00GAR1WAS3DO01        = StringField(SzenenDatabase.get_description('A00GAR1WAS3DO01')+': '+'A00GAR1WAS3DO01')       
    A00GAR1WAS2DO01        = StringField(SzenenDatabase.get_description('A00GAR1WAS2DO01')+': '+'A00GAR1WAS2DO01')       
    A00RAS1MAE1DO01        = StringField(SzenenDatabase.get_description('A00RAS1MAE1DO01')+': '+'A00RAS1MAE1DO01')       
    A00TER1ADV1ST01        = StringField(SzenenDatabase.get_description('A00TER1ADV1ST01')+': '+'A00TER1ADV1ST01')       
    A00TER1DEK1LI01        = StringField(SzenenDatabase.get_description('A00TER1DEK1LI01')+': '+'A00TER1DEK1LI01')       
    A00TER1GEN1LI01        = StringField(SzenenDatabase.get_description('A00TER1GEN1LI01')+': '+'A00TER1GEN1LI01')       
    A00TER1GEN1PO01        = StringField(SzenenDatabase.get_description('A00TER1GEN1PO01')+': '+'A00TER1GEN1PO01')       
    A00TER1GEN1ST01        = StringField(SzenenDatabase.get_description('A00TER1GEN1ST01')+': '+'A00TER1GEN1ST01') 
    A00TER1DEK1DO01        = StringField(SzenenDatabase.get_description('A00TER1DEK1DO01')+': '+'A00TER1DEK1DO01')
    A00TER2MAR1DO01        = StringField(SzenenDatabase.get_description('A00TER2MAR1DO01')+': '+'A00TER2MAR1DO01')
    A00TER2MAR1DO02        = StringField(SzenenDatabase.get_description('A00TER2MAR1DO02')+': '+'A00TER2MAR1DO02')
    A00TER2MAR1DO03        = StringField(SzenenDatabase.get_description('A00TER2MAR1DO03')+': '+'A00TER2MAR1DO03')   
    A00TER2MAR1DO99        = StringField(SzenenDatabase.get_description('A00TER2MAR1DO99')+': '+'A00TER2MAR1DO99') 
    A00TER2MAR1PO01        = StringField(SzenenDatabase.get_description('A00TER2MAR1PO01')+': '+'A00TER2MAR1PO01') # Strom Markise

class SzenenFormEG(FlaskForm):
    V00ESS1DEK1LI01        = StringField(SzenenDatabase.get_description('V00ESS1DEK1LI01')+': '+'V00ESS1DEK1LI01')       
    V00ESS1RUM1LI01        = StringField(SzenenDatabase.get_description('V00ESS1RUM1LI01')+': '+'V00ESS1RUM1LI01')       
    V00ESS1OUT1PO01        = StringField(SzenenDatabase.get_description('V00ESS1OUT1PO01')+': '+'V00ESS1OUT1PO01')       
    V00FLU1DEK1LI01        = StringField(SzenenDatabase.get_description('V00FLU1DEK1LI01')+': '+'V00FLU1DEK1LI01')       
    V00FLU1SRA1LI01        = StringField(SzenenDatabase.get_description('V00FLU1SRA1LI01')+': '+'V00FLU1SRA1LI01')       
    V00FLU1TUE1DO03        = StringField(SzenenDatabase.get_description('V00FLU1TUE1DO03')+': '+'V00FLU1TUE1DO03')       
    V00FLU1TUE1DO03conf    = StringField(SzenenDatabase.get_description('V00FLU1TUE1DO03conf')+': '+'V00FLU1TUE1DO03conf')   
    V00FLU1TUE1PC01        = StringField(SzenenDatabase.get_description('V00FLU1TUE1PC01')+': '+'V00FLU1TUE1PC01')       
    V00KUE1ZIM1PO01        = StringField(SzenenDatabase.get_description('V00KUE1ZIM1PO01')+': '+'V00KUE1ZIM1PO01')       
    V00KUE1ADV1LI01        = StringField(SzenenDatabase.get_description('V00KUE1ADV1LI01')+': '+'V00KUE1ADV1LI01')       
    V00KUE1DEK1LI01        = StringField(SzenenDatabase.get_description('V00KUE1DEK1LI01')+': '+'V00KUE1DEK1LI01')       
    V00KUE1DEK1LI02        = StringField(SzenenDatabase.get_description('V00KUE1DEK1LI02')+': '+'V00KUE1DEK1LI02')       
    V00KUE1RUM1AV11        = StringField(SzenenDatabase.get_description('V00KUE1RUM1AV11')+': '+'V00KUE1RUM1AV11')       
    V00KUE1RUM1LI01        = StringField(SzenenDatabase.get_description('V00KUE1RUM1LI01')+': '+'V00KUE1RUM1LI01')       
    V00KUE1RUM1ST01        = StringField(SzenenDatabase.get_description('V00KUE1RUM1ST01')+': '+'V00KUE1RUM1ST01')       
    V00KUE1RUM1TE01        = StringField(SzenenDatabase.get_description('V00KUE1RUM1TE01')+': '+'V00KUE1RUM1TE01')       
    V00KUE1SRA1LI01        = StringField(SzenenDatabase.get_description('V00KUE1SRA1LI01')+': '+'V00KUE1SRA1LI01')       
    V00TOI1DEK1LI01        = StringField(SzenenDatabase.get_description('V00TOI1DEK1LI01')+': '+'V00TOI1DEK1LI01')       
    V00TRE1RUM1AL01        = StringField(SzenenDatabase.get_description('V00TRE1RUM1AL01')+': '+'V00TRE1RUM1AL01')       
    V00TRE1RUM1AL02        = StringField(SzenenDatabase.get_description('V00TRE1RUM1AL02')+': '+'V00TRE1RUM1AL02')       
    V00TRE1RUM1AL03        = StringField(SzenenDatabase.get_description('V00TRE1RUM1AL03')+': '+'V00TRE1RUM1AL03')       
    V00TRE1RUM1LI01        = StringField(SzenenDatabase.get_description('V00TRE1RUM1LI01')+': '+'V00TRE1RUM1LI01')       
    V00WOH1ADV1LI01        = StringField(SzenenDatabase.get_description('V00WOH1ADV1LI01')+': '+'V00WOH1ADV1LI01')       
    V00WOH1ADV1LI02        = StringField(SzenenDatabase.get_description('V00WOH1ADV1LI02')+': '+'V00WOH1ADV1LI02')       
    V00WOH1DEK1LI01        = StringField(SzenenDatabase.get_description('V00WOH1DEK1LI01')+': '+'V00WOH1DEK1LI01')       
    V00WOH1RUM1AV01        = StringField(SzenenDatabase.get_description('V00WOH1RUM1AV01')+': '+'V00WOH1RUM1AV01')       
    V00WOH1RUM1AV11        = StringField(SzenenDatabase.get_description('V00WOH1RUM1AV11')+': '+'V00WOH1RUM1AV11')       
    V00WOH1RUM1DI01        = StringField(SzenenDatabase.get_description('V00WOH1RUM1DI01')+': '+'V00WOH1RUM1DI01')       
    V00WOH1RUM1DO10        = StringField(SzenenDatabase.get_description('V00WOH1RUM1DO10')+': '+'V00WOH1RUM1DO10')       
    V00WOH1RUM1LI11        = StringField(SzenenDatabase.get_description('V00WOH1RUM1LI11')+': '+'V00WOH1RUM1LI11')       
    V00WOH1RUM1LI12        = StringField(SzenenDatabase.get_description('V00WOH1RUM1LI12')+': '+'V00WOH1RUM1LI12')       
    V00WOH1RUM1LI13        = StringField(SzenenDatabase.get_description('V00WOH1RUM1LI13')+': '+'V00WOH1RUM1LI13')       
    V00WOH1RUM1LI14        = StringField(SzenenDatabase.get_description('V00WOH1RUM1LI14')+': '+'V00WOH1RUM1LI14')       
    V00WOH1RUM1PC01        = StringField(SzenenDatabase.get_description('V00WOH1RUM1PC01')+': '+'V00WOH1RUM1PC01')       
    V00WOH1RUM1ST01        = StringField(SzenenDatabase.get_description('V00WOH1RUM1ST01')+': '+'V00WOH1RUM1ST01')       
    V00WOH1RUM1ST02        = StringField(SzenenDatabase.get_description('V00WOH1RUM1ST02')+': '+'V00WOH1RUM1ST02')       
    V00WOH1RUM1TV01        = StringField(SzenenDatabase.get_description('V00WOH1RUM1TV01')+': '+'V00WOH1RUM1TV01')       
    V00WOH1SRA1LI01        = StringField(SzenenDatabase.get_description('V00WOH1SRA1LI01')+': '+'V00WOH1SRA1LI01')       
    V00WOH1SRA1LI02        = StringField(SzenenDatabase.get_description('V00WOH1SRA1LI02')+': '+'V00WOH1SRA1LI02')       
    V00WOH1SRA1LI03        = StringField(SzenenDatabase.get_description('V00WOH1SRA1LI03')+': '+'V00WOH1SRA1LI03')       
    V00WOH1SRA1LI04        = StringField(SzenenDatabase.get_description('V00WOH1SRA1LI04')+': '+'V00WOH1SRA1LI04')       
    V00WOH1SRA1LI11        = StringField(SzenenDatabase.get_description('V00WOH1SRA1LI11')+': '+'V00WOH1SRA1LI11')       
    V00WOH1SRA1PC01        = StringField(SzenenDatabase.get_description('V00WOH1SRA1PC01')+': '+'V00WOH1SRA1PC01')       
    V00WOH1STV01           = StringField(SzenenDatabase.get_description('V00WOH1STV01')+': '+'V00WOH1STV01')          
    V00WOH1STV02           = StringField(SzenenDatabase.get_description('V00WOH1STV02')+': '+'V00WOH1STV02')          
    V00WOH1TUR1LI01        = StringField(SzenenDatabase.get_description('V00WOH1TUR1LI01')+': '+'V00WOH1TUR1LI01')       
      

class SzenenFormOG(FlaskForm):
    V01BAD1DEK1LI01        = StringField(SzenenDatabase.get_description('V01BAD1DEK1LI01')+': '+'V01BAD1DEK1LI01')       
    V01BAD1DEK1LI02        = StringField(SzenenDatabase.get_description('V01BAD1DEK1LI02')+': '+'V01BAD1DEK1LI02')       
    V01BAD1RUM1AV11        = StringField(SzenenDatabase.get_description('V01BAD1RUM1AV11')+': '+'V01BAD1RUM1AV11')       
    V01BAD1RUM1LI02        = StringField(SzenenDatabase.get_description('V01BAD1RUM1LI02')+': '+'V01BAD1RUM1LI02')       
    V01BUE1DEK1LI01        = StringField(SzenenDatabase.get_description('V01BUE1DEK1LI01')+': '+'V01BUE1DEK1LI01')       
    V01BUE1STL1DO01        = StringField(SzenenDatabase.get_description('V01BUE1STL1DO01')+': '+'V01BUE1STL1DO01')       
    V01FLU1DEK1LI01        = StringField(SzenenDatabase.get_description('V01FLU1DEK1LI01')+': '+'V01FLU1DEK1LI01')       
    V01KID1DEK1LI01        = StringField(SzenenDatabase.get_description('V01KID1DEK1LI01')+': '+'V01KID1DEK1LI01')       
    V01KID1RUM1AV11        = StringField(SzenenDatabase.get_description('V01KID1RUM1AV11')+': '+'V01KID1RUM1AV11')       
    V01KID1RUM1LI02        = StringField(SzenenDatabase.get_description('V01KID1RUM1LI02')+': '+'V01KID1RUM1LI02')       
    V01KID1ZIM1ST01        = StringField(SzenenDatabase.get_description('V01KID1ZIM1ST01')+': '+'V01KID1ZIM1ST01')       
    V01KID1ZIM1ST02        = StringField(SzenenDatabase.get_description('V01KID1ZIM1ST02')+': '+'V01KID1ZIM1ST02')       
    V01SCH1BET1LI01        = StringField(SzenenDatabase.get_description('V01SCH1BET1LI01')+': '+'V01SCH1BET1LI01')       
    V01SCH1BET1LI02        = StringField(SzenenDatabase.get_description('V01SCH1BET1LI02')+': '+'V01SCH1BET1LI02')       
    V01SCH1DEK1LI01        = StringField(SzenenDatabase.get_description('V01SCH1DEK1LI01')+': '+'V01SCH1DEK1LI01')       
    V01SCH1RUM1AV11        = StringField(SzenenDatabase.get_description('V01SCH1RUM1AV11')+': '+'V01SCH1RUM1AV11')       
    V01SCH1RUM1LI02        = StringField(SzenenDatabase.get_description('V01SCH1RUM1LI02')+': '+'V01SCH1RUM1LI02')       
    V01SCH1RUM1LI10        = StringField(SzenenDatabase.get_description('V01SCH1RUM1LI10')+': '+'V01SCH1RUM1LI10')       
    V01SCH1RUM1LI11        = StringField(SzenenDatabase.get_description('V01SCH1RUM1LI11')+': '+'V01SCH1RUM1LI11') 
    V01SCH1RUM1PO01        = StringField(SzenenDatabase.get_description('V01SCH1RUM1PO01')+': '+'V01SCH1RUM1PO01') # Strom Steckdosen
    V01SCH1STE1LI01        = StringField(SzenenDatabase.get_description('V01SCH1STE1LI01')+': '+'V01SCH1STE1LI01')       
    V01SCH1STE1LI02        = StringField(SzenenDatabase.get_description('V01SCH1STE1LI02')+': '+'V01SCH1STE1LI02') 
    V01KID1ZIM1LI01        = StringField(SzenenDatabase.get_description('V01KID1ZIM1LI01')+': '+'V01KID1ZIM1LI01') 
    V01KID1UIM1LI02        = StringField(SzenenDatabase.get_description('V01KID1UIM1LI02')+': '+'V01KID1UIM1LI02')            

class SzenenFormUG(FlaskForm):
    VIRKOM1SSH1PC01        = StringField(SzenenDatabase.get_description('VIRKOM1SSH1PC01')+': '+'VIRKOM1SSH1PC01')       
    VIRKOM1SSH1PC02        = StringField(SzenenDatabase.get_description('VIRKOM1SSH1PC02')+': '+'VIRKOM1SSH1PC02')       
    VIRKOM1SSH1PC03        = StringField(SzenenDatabase.get_description('VIRKOM1SSH1PC03')+': '+'VIRKOM1SSH1PC03')       
    VIRKOM1SSH1PC04        = StringField(SzenenDatabase.get_description('VIRKOM1SSH1PC04')+': '+'VIRKOM1SSH1PC04')       
    VIRKOM1SSH1PC05        = StringField(SzenenDatabase.get_description('VIRKOM1SSH1PC05')+': '+'VIRKOM1SSH1PC05')       
    Vm1FLU1DEK1LI01        = StringField(SzenenDatabase.get_description('Vm1FLU1DEK1LI01')+': '+'Vm1FLU1DEK1LI01')       
    Vm1GAR1PAR1LI01        = StringField(SzenenDatabase.get_description('Vm1GAR1PAR1LI01')+': '+'Vm1GAR1PAR1LI01')       
    Vm1GAR1TUR1DI01        = StringField(SzenenDatabase.get_description('Vm1GAR1TUR1DI01')+': '+'Vm1GAR1TUR1DI01')       
    Vm1ZIM1DEK1LI01        = StringField(SzenenDatabase.get_description('Vm1ZIM1DEK1LI01')+': '+'Vm1ZIM1DEK1LI01')       
    Vm1ZIM1PFL1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM1PFL1DO01')+': '+'Vm1ZIM1PFL1DO01')       
    Vm1ZIM1PFL1LI01        = StringField(SzenenDatabase.get_description('Vm1ZIM1PFL1LI01')+': '+'Vm1ZIM1PFL1LI01')       
    Vm1ZIM1RUM1AV11        = StringField(SzenenDatabase.get_description('Vm1ZIM1RUM1AV11')+': '+'Vm1ZIM1RUM1AV11')       
    Vm1ZIM1RUM1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM1RUM1DO01')+': '+'Vm1ZIM1RUM1DO01')       
    Vm1ZIM1RUM1ST01        = StringField(SzenenDatabase.get_description('Vm1ZIM1RUM1ST01')+': '+'Vm1ZIM1RUM1ST01')       
    Vm1ZIM1RUT1PC01        = StringField(SzenenDatabase.get_description('Vm1ZIM1RUT1PC01')+': '+'Vm1ZIM1RUT1PC01')       
    Vm1ZIM1SAT1LI01        = StringField(SzenenDatabase.get_description('Vm1ZIM1SAT1LI01')+': '+'Vm1ZIM1SAT1LI01')       
    Vm1ZIM1SCA1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM1SCA1DO01')+': '+'Vm1ZIM1SCA1DO01')       
    Vm1ZIM1SEV1PC01        = StringField(SzenenDatabase.get_description('Vm1ZIM1SEV1PC01')+': '+'Vm1ZIM1SEV1PC01')       
    Vm1ZIM1TUR1DO10        = StringField(SzenenDatabase.get_description('Vm1ZIM1TUR1DO10')+': '+'Vm1ZIM1TUR1DO10')       
    Vm1ZIM2DEK1LI01        = StringField(SzenenDatabase.get_description('Vm1ZIM2DEK1LI01')+': '+'Vm1ZIM2DEK1LI01')       
    Vm1ZIM2NAT1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM2NAT1DO01')+': '+'Vm1ZIM2NAT1DO01')       
    Vm1ZIM2TRO1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM2TRO1DO01')+': '+'Vm1ZIM2TRO1DO01')       
    Vm1ZIM2WAS1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM2WAS1DO01')+': '+'Vm1ZIM2WAS1DO01')       
    Vm1ZIM3DEK1LI01        = StringField(SzenenDatabase.get_description('Vm1ZIM3DEK1LI01')+': '+'Vm1ZIM3DEK1LI01')       
    Vm1ZIM3RUM1ST01        = StringField(SzenenDatabase.get_description('Vm1ZIM3RUM1ST01')+': '+'Vm1ZIM3RUM1ST01')       
    Vm1ZIM3STR1DO01        = StringField(SzenenDatabase.get_description('Vm1ZIM3STR1DO01')+': '+'Vm1ZIM3STR1DO01')         
   #    V01KID1UIM1LI02        = StringField('V01KID1UIM1LI02')       
class SzenenFormDG(FlaskForm):
    V02BAD1DEK1LI01        = StringField(SzenenDatabase.get_description('V02BAD1DEK1LI01')+': '+'V02BAD1DEK1LI01')       
    V02TRE1DEK1LI01        = StringField(SzenenDatabase.get_description('V02TRE1DEK1LI01')+': '+'V02TRE1DEK1LI01')       
    V02ZIM1DEK1LI01        = StringField(SzenenDatabase.get_description('V02ZIM1DEK1LI01')+': '+'V02ZIM1DEK1LI01')       
    V02ZIM1RUM1ST01        = StringField(SzenenDatabase.get_description('V02ZIM1RUM1ST01')+': '+'V02ZIM1RUM1ST01') 
    V00ZIM0RUM0DO01        = StringField(SzenenDatabase.get_description('V00ZIM0RUM0DO01')+': '+'V00ZIM0RUM0DO01')       
    V00ZIM0RUM0DO02        = StringField(SzenenDatabase.get_description('V00ZIM0RUM0DO02')+': '+'V00ZIM0RUM0DO02')     

class SzenenFormStore(FlaskForm):
    V00KUE1FEN1SR01        = StringField(SzenenDatabase.get_description('V00KUE1FEN1SR01')+': '+'V00KUE1FEN1SR01')       
    V00ESS1TUR1SR01        = StringField(SzenenDatabase.get_description('V00ESS1TUR1SR01')+': '+'V00ESS1TUR1SR01')       
    V00WOH1FEN1SR01        = StringField(SzenenDatabase.get_description('V00WOH1FEN1SR01')+': '+'V00WOH1FEN1SR01')       
    V00WOH1TUR1SR01        = StringField(SzenenDatabase.get_description('V00WOH1TUR1SR01')+': '+'V00WOH1TUR1SR01') 
    
    V01BAD1FEN1SR01        = StringField(SzenenDatabase.get_description('V01BAD1FEN1SR01')+': '+'V01BAD1FEN1SR01')       
    V01SCH1FEN1SR01        = StringField(SzenenDatabase.get_description('V01SCH1FEN1SR01')+': '+'V01SCH1FEN1SR01')     
    V01SCH1FEN2SR01        = StringField(SzenenDatabase.get_description('V01SCH1FEN2SR01')+': '+'V01SCH1FEN2SR01')  
    V01BUE1FEN1SR01        = StringField(SzenenDatabase.get_description('V01BUE1FEN1SR01')+': '+'V01BUE1FEN1SR01')  
    V01BUE1FEN2SR01        = StringField(SzenenDatabase.get_description('V01BUE1FEN2SR01')+': '+'V01BUE1FEN2SR01')  
    V01KID1FEN1SR01        = StringField(SzenenDatabase.get_description('V01KID1FEN1SR01')+': '+'V01KID1FEN1SR01')  

    V02ZIM1FEN1SR01        = StringField(SzenenDatabase.get_description('V02ZIM1FEN1SR01')+': '+'V02ZIM1FEN1SR01')  
    V02ZIM1FEN2SR01        = StringField(SzenenDatabase.get_description('V02ZIM1FEN2SR01')+': '+'V02ZIM1FEN2SR01')      

@app.route('/inputs/')
def index_inputs(Scene=None):
    sort = request.args.get('sort', 'Id')
    Name = request.args.get('Name', '')
    filtHKS = request.args.get('HKS', '')
    filtDesc = request.args.get('Desc', '') 
    if not Scene:
        Scene = request.args.get('Scene', '')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTableInputs(InputsDatabase.get_sorted_by(sort, reverse, Name, filtHKS, filtDesc,Scene),
                          sort_by=sort,
                          sort_reverse=reverse,
                          border=True)
    return table.__html__()

@app.route('/inputs/new/<int:Id>')
def new_trig(Id):
    InputsDatabase.new_trigger(Id)
    return 'New Trigger created'

@app.route('/inputs/delete/<int:Id>', methods=['GET', 'POST'])
def delete_id(Id):    
    if request.method == 'POST':
        print('delete ID')
        InputsDatabase.del_element(Id)
        return 'ID deleted'
    elif request.method == 'GET':
        return render_template('delete_form.html')    


@app.route('/inputs/item/<int:Id>', methods=['GET', 'POST'])
def flask_link(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    filtGruppe = request.args.get('filterGruppe', None)
    error = ""
    element  = InputsDatabase.get_element_by_id(Id)
    elements = InputsDatabase.get_elements_by_name(element.Name)
    form = TriggerForm()
#    form_action = url_for('index')
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                if item in ['Immer', 'Wach', 'Sturm']:
                    setattr(getattr(form, item), 'choices', SzenenDatabase.get_all_names(filtGruppe))                
                setattr(getattr(form, item),'data',getattr(element, item))
                if item in ['Logging', 'Doppelklick','enabled', 'debug','Kompression','latch_always']:
                    setattr(getattr(form, item),'data', str(getattr(element, item)))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_iptDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_iptDB[item][1]))
            if item in device_props:
                for subel in elements:
                    if item in subel.__dict__:
                        setattr(subel, item, convert_to(getattr(getattr(form, item), 'data'), properties_iptDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('flask_link', Id=Id))

    # Render the sign-up page
    return render_template('input_el_template.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/')
def index_szenen():
    sort = request.args.get('sort', 'Id')
    Id = request.args.get('Id', '')
    filtName = request.args.get('Name', '')
    filterDesc = request.args.get('Beschreibung', '')
    filterGruppe = request.args.get('Gruppe', '')  
    Setting = request.args.get('Setting', '')
    Follows = request.args.get('Follows', '')
    Bedingung = request.args.get('Bedingung', '')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    kwargs = {}
    for key, value in properties_sznDB.items():
        if any([i in key for i in ['V0', 'Vm', 'A0', 'VIR']]):
            kwargs[key] = request.args.get(key, '')    
    table = SortableTableSzenen(SzenenDatabase.get_sorted_by(sort, reverse, Id, filtName, filterDesc, filterGruppe, Setting, Follows, Bedingung, **kwargs),
                          sort_by=sort,
                          sort_reverse=reverse,
                          border=True)
    return table.__html__()

@app.route('/execScene/<int:Id>', methods=['GET', 'POST'])
def execScene(Scene=None, Id=None):
    if not Scene:
        Scene = request.args.get('Scene', None)    
    payload = {'Szene':Scene}
    toolbox.communication.send_message(payload, typ='ExecSzene')   
    return redirect(url_for('index_szenen', Id=Id))

@app.route('/szenen/delete/<int:Id>', methods=['GET', 'POST'])
def delete_szene(Id):    
    if request.method == 'POST':
        print('delete Szene')
        SzenenDatabase.del_element(Id)
        return 'Szene deleted'
    elif request.method == 'GET':
        return render_template('delete_form.html') 

@app.route('/szenen/item/<int:Id>', methods=['GET', 'POST'])
def edit_szn(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenForm()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',str(getattr(element, item)))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))  
#        return 'thank_you'
        return redirect(url_for('edit_szn', Id=Id))

    # Render the sign-up page
    return render_template('szn_el_template.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/item/ug/<int:Id>', methods=['GET', 'POST'])
def edit_szn_ug(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormUG()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                   
#        return 'thank_you'
        return redirect(url_for('edit_szn_ug', Id=Id))

    # Render the sign-up page
    return render_template('szn_ug.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/item/eg/<int:Id>', methods=['GET', 'POST'])
def edit_szn_eg(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormEG()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('edit_szn_eg', Id=Id))

    # Render the sign-up page
    return render_template('szn_eg.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/item/og/<int:Id>', methods=['GET', 'POST'])
def edit_szn_og(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormOG()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('edit_szn_og', Id=Id))

    # Render the sign-up page
    return render_template('szn_og.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/item/dg/<int:Id>', methods=['GET', 'POST'])
def edit_szn_dg(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormDG()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('edit_szn_dg', Id=Id))

    # Render the sign-up page
    return render_template('szn_dg.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action
    
@app.route('/szenen/item/a/<int:Id>', methods=['GET', 'POST'])
def edit_szn_a(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormA()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('edit_szn_a', Id=Id))

    # Render the sign-up page
    return render_template('szn_a.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/item/storen/<int:Id>', methods=['GET', 'POST'])
def edit_szn_store(Id=None):
    if not Id:
        Id = request.args.get('Id', 1)
    error = ""
    element  = SzenenDatabase.get_element_by_id(Id)
    form = SzenenFormStore()
    if request.method == 'GET':
        for item, value in form.__dict__.items():
            if item in element.__dict__:
                setattr(getattr(form, item),'data',getattr(element, item))
    if request.method == 'POST':
        for item, value in form.__dict__.items():
            if item in element.__dict__ and item in properties_sznDB:
                setattr(element, item, convert_to(getattr(getattr(form, item), 'data'), properties_sznDB[item][1]))                    
#        return 'thank_you'
        return redirect(url_for('edit_szn_store', Id=Id))

    # Render the sign-up page
    return render_template('szn_store.html', message=error, form=form, Id=Id,
                                title="Update Profile") #form_action=form_action

@app.route('/szenen/copy/<int:Id>')
def copy_szene(Id):
    new_id = SzenenDatabase.copy_szene(Id)
    return redirect(url_for('index_szenen', Id=new_id))

datab = constants.sql_.DB

validTimers = {}
sturmTimers = {}
locklist = {}
persTimers = {}

inputs_dict = {}
prozessspiegel = {}





def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return 'not json serializable' #TypeError ("Type %s not serializable" % type(obj))


def invalidTimers(device, desc):
    print('input timed out: ', desc)
    hkses = InputsDatabase.get_elements_by_name(device)
    # erstmal überprüfen....
    if hkses and hkses[0].time and hkses[0].heartbeat:
        ct = datetime.datetime.now()
        timout = hkses[0].time + datetime.timedelta(seconds=hkses[0].heartbeat)
        if ct < timout:
            print('Nein doch nicht: ', desc)
            return None
    for item in hkses:
        item.valid = False
    if hkses and hkses[0].fallback:
        inputs(hkses[0].Name, hkses[0].fallback, fallingback=True)
#    validTimers.remove(hks)
    validTimers.pop(device, None)
    with open('hrtbt_timer.jsn', 'w') as fout:
        json.dump(validTimers, fout, default=json_serial)        
    payload = {'Szene':'InputTimedOut', 'desc':'input timed out: '+ desc}
    toolbox.communication.send_message(payload, typ='ExecSzene')          

def resetSturm(trigger):
    InputsDatabase.set_val_by_name(trigger.Name, 'Sturm_count', 0)


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
                    invalidTimers(device, desc)
                else:
                    thread_pt_ = Timer(delay, invalidTimers, [device, desc])
                    thread_pt_.start()
                    entry['timer'] = thread_pt_
                    validTimers[device] = entry 
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
    tries = 0
    retries = 4
    while tries < retries:
        try:
            json_body = [{"measurement": key,
                          "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                          "fields": {"value": str(value)}}]
            client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
            if client.write_points(json_body):
                tries = retries
        except:
            tries += 1
            print(key, value, utc)
    return True 

def get_input_value(hks):
    """ returns the value from an input device
    """
#    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    value = None
#    with con:
#        cur = con.cursor()
#        cur.execute("SELECT last_Value FROM %s.%s WHERE HKS = '%s'" % (datab, constants.sql_tables.inputs.name, hks))
##        if cur.fetchone()[0] != 0:
##            con.close()
##            return False
#        results = cur.fetchall()
#        for row in results:
#            value = row[0]
#    con.close()
    triggers = [item for item in InputsDatabase.elements if item.HKS == hks]
    if triggers:
        value = triggers[0].Value
    return value

def inputs_r():
#    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    dicti = InputsDatabase.get_all_vals_as_dict()
#    with con:
#        cur = con.cursor()
#        sql = 'SELECT HKS, last_Value FROM '+constants.sql_tables.inputs.name
#        cur.execute(sql)
#        results = cur.fetchall()
##        field_names = [i[0] for i in cur.description]
#        for row in results:
#            dicti[row[0]] = str(row[1])
#    con.close()
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
        data = {'Value':str(wert), 'Setting':str(setting)}
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
    items = [item.valid for item in InputsDatabase.elements if item.HKS == inpt]
    if items:
        return items[0]
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
#    temp_res = mdb_read_table_entry(constants.sql_tables.szenen.name, 'Value')
#    return temp_res[hks]
    return SzenenDatabase.get_val_in_szenen(hks,'Value')

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
#    db = constants.sql_tables.inputs.name
#    column = 'description'
#    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = [item.Description for item in InputsDatabase.elements if item.valid == False]
    rlist = list(set(rlist))
#    with con:
#        cur = con.cursor()
#        #SELECT * FROM Steuerzentrale.HIS_inputs where Name like '%Rose%' order by id desc limit 1000;
#        sql = 'SELECT %s FROM %s WHERE valid LIKE "False" ORDER BY ID %s LIMIT %s' % (column, db, order, amount)
#        cur.execute(sql)
#        results = cur.fetchall()
#        for row in results:
#            rlist.append(row[0])
#            if type(row[0]) == datetime.datetime:
#                rlist.append((int(row[0].strftime("%s"))))
#            else:
#                rlist.append(eval(str(row[0])))
#    con.close()
    return rlist

def ack_bdq(desc):
    for item in InputsDatabase.elements:
        if item.Description == desc:
            item.valid= True

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
#    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
#    value = 0
#    with con:
#        cur = con.cursor()
#        cur.execute("SELECT %s FROM %s.%s WHERE ID = '6'" % (device, datab, constants.sql_tables.szenen.name))
##        if cur.fetchone()[0] != 0:
#        results = cur.fetchall()
#        for row in results:
#            value = row[0]
#    con.close()
#    return value
    return SzenenDatabase.get_val_in_szenen(device,'Adress')


#def getSzenenSources(szene):
#    # für gui veraltet
#    if szene in ['', None]:
#        return [],[]
#    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
#    ilist, slist = [], []
#    with con:
#        cur = con.cursor()
#        sql = 'SELECT * FROM '+constants.sql_tables.inputs.name+' where "'+szene+\
#              '" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach, Alarm)'
#        sql = 'SELECT * FROM %s where "%s" in (Wach, Schlafen, Schlummern, Leise, AmGehen, Gegangen, Abwesend, Urlaub, Besuch, Doppel, Dreifach, Alarm)' % (constants.sql_tables.inputs.name, szene)
#        cur.execute(sql)
#        results = cur.fetchall()
#        field_names = [i[0] for i in cur.description]
#        for row in results:
#            dicti = {}
#            for i in range (0,len(row)):
#               dicti[field_names[i]] = row[i]
#            ilist.append(dicti)
#        sql = 'SELECT * FROM '+constants.sql_tables.szenen.name+' where Follows like "%'+szene+'%"'
#        szene = "%" + szene + "%"
#        sql = 'SELECT * FROM %s.%s where Follows like "%s"' % (datab, constants.sql_tables.szenen.name, szene)
#        cur.execute(sql)
#        results = cur.fetchall()
#        field_names = [i[0] for i in cur.description]
#        for row in results:
#            dicti = {}
#            for i in range (0,len(row)):
#               dicti[field_names[i]] = row[i]
#            slist.append(dicti)
#    con.close()
#    return ilist, slist

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
        pass
#        print(sql, counter)

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
#    global inputs_table
    ct = datetime.datetime.now()
    utc = datetime.datetime.utcnow()
#    if 'inputs' in device:
#        print(value,device)
    set_inval = False
    try:
        if 'invalid' in value:
            set_inval = True
            value = 0
    except Exception as e:
        pass
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
    #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    
    #dicti_1 = {}
    alle_szenen = []
    alle_payloads = []
    descriptions = []
    desc = None
    heartbt = None
    filtered = False
    writeToInflx = False
    hks = device
    
    results2, last_val = InputsDatabase.new_value(device, value, ct, fallingback)


#        cur = con.cursor()
#        cur.execute("SELECT COUNT(*) FROM "+datab+"."+constants.sql_tables.inputs.name+" WHERE Name = '"+device+"'")
#        if not device in [item['Name'] for key, item in inputs_table.items()]:
#        if cur.fetchone()[0] == 0:
    if True:
#            sql = 'INSERT INTO '+constants.sql_tables.inputs.name+' (Name, HKS, Description, Logging, Setting, Doppelklick) VALUES ("' + str(device) + '","' + str(device) + '","' + str(device) + '","True","False","False")'
#            cur.execute(sql)
#        else:
#            get last value and last time
#            sql = 'SELECT * FROM %s WHERE Name = "%s"' % (constants.sql_tables.inputs.name, str(device))
#            cur.execute(sql)
#            results_1 = cur.fetchall()
#            field_names_1 = [i[0] for i in cur.description]
#            for row in results_1:
#                for i in range (0,len(row)):
#                    dicti_1[field_names_1[i]] = row[i]
#            last_value = dicti_1['last_Value']         
                
        trigger_0 = results2[0]
        last_value = last_val            
        
        # wenn wir dann interne sachen nehmen:
#            inputs_table_c = copy.copy(inputs_table)                    
        #dicti_2 = results2[device]
                   
        # Filtern, wenn groesser oder kleiner Messung ignorieren
#            filtering = dicti_1['Filter']
        filtering = trigger_0.Filter
#            hks = dicti_1['HKS']
        hks = trigger_0.HKS
        # könnte fallingback auch vorher definieren
#            if fallingback and dicti_1['fallback'] is not None:
        if fallingback and trigger_0.fallback is not None:
#                value = float(dicti_1['fallback'])
            value = float(trigger_0.fallback)
        try:
            filtering = eval(filtering)
        except:
            filtering = [None, None]
        if filtering[0]:
            if value <= filtering[0]:
                filtered = True
        if filtering[1]:
            if value >= filtering[1]:
                filtered = True
        if not trigger_0.Sturm_anz is None and not trigger_0.Sturm_dauer is None: 
            if not trigger_0.Sturm_count is None:
                InputsDatabase.set_val_by_name(trigger_0.Name, 'Sturm_count', trigger_0.Sturm_count + 1)
                if trigger_0.Sturm_count >= trigger_0.Sturm_anz:
                    filtered = True
                    if trigger_0.Sturm:
                        payload = {'Szene':trigger_0.Sturm, 'desc':trigger_0.Description}
                        toolbox.communication.send_message(payload, typ='ExecSzene')   
            else:
                InputsDatabase.set_val_by_name(trigger_0.name, 'Sturm_count', 0)
                
        if not filtered:        
#                valid =   dicti_1['valid']
#                heartbt = dicti_1['heartbeat']
#                desc =    dicti_1['Description']
#                komp =    dicti_1['Kompression']
#                hyst =    dicti_1['Hysterese']
#                recSzn =  dicti_1['RecoverSzn']
#                offset =  dicti_1['offset']
#                last1 =   dicti_1['last1']
#                debounce = dicti_1['debounce']
            
            valid =   trigger_0.valid
            heartbt = trigger_0.heartbeat
            desc =    trigger_0.Description
            komp =    trigger_0.Kompression
            hyst =    trigger_0.Hysterese
            recSzn =  trigger_0.RecoverSzn
            offset =  trigger_0.offset
            last1 =   trigger_0.last1
            lc    =   trigger_0.lastChange

            if not lc:
                lc = ct
            frozenTime = lc                
            if trigger_0.frozen:
                frozenTime = lc + datetime.timedelta(seconds=trigger_0.frozen)
#                last1 =   datetime.datetime.strptime(trigger_0.last1, '%Y-%m-%dT%H:%M:%S.%f')
            debounce = trigger_0.debounce
            if type(debounce) == str and len(debounce) == 0:
                debounce = 0
            if debounce:
                debounce = int(debounce)
            
#                if trigger_0.Name == 'TiFo.6QGwm1.vYN.a0b1':
#                    print(value, last_value, komp)
            
            if str(offset) != 'None':
                if type(offset) == str and len(offset) == 0:
                    offset = 0
                offset = float(offset)
                value = value + offset
            if not valid and not fallingback and not persTimer and not set_inval:  # das hier ist fürs Timeout 
                if (not trigger_0.frozen) or ((last_value != value) or (frozenTime > ct)):# das ist wenn der Wert eingefroren ist
                    for trigger in results2:
                        trigger.valid = True                 
                    payload = {'Szene':'InputTimedOut', 'desc':'input recovered: '+ desc}
                    toolbox.communication.send_message(payload, typ='ExecSzene')
                    if recSzn:
                        payload = {'Szene':recSzn}
                        toolbox.communication.send_message(payload, typ='ExecSzene') 
            if valid and not fallingback and not persTimer:
                if trigger_0.frozen and (frozenTime < ct) and (last_value == value): 
                    payload = {'Szene':'InputTimedOut', 'desc':'Wert eingefroren: '+ desc}
                    toolbox.communication.send_message(payload, typ='ExecSzene')                    
                    for trigger in results2:
                        trigger.valid = False
            if set_inval:
                payload = {'Szene':'InputTimedOut', 'desc':'Wert invaliditiert: '+ desc}
                toolbox.communication.send_message(payload, typ='ExecSzene')                    
                for trigger in results2:
                    trigger.valid = False                
            if not fallingback and not persTimer and (last_value != value):
                for trigger in results2:
                    trigger.lastChange = ct                
            if last_value is None: 
                last_value = value
                writeToInflx = True
            elif float(last_value) != value:
                writeToInflx = True
            if str(komp) in ['None', 'False']:
                writeToInflx = True
            if str(komp) in ['Bool']:
                if (float(last_value) <= 0.0 and value >= 0.0) or (float(last_value) >= 0.0 and value <= 0.0):
                    writeToInflx = True   
                else:
                    writeToInflx = False
            if not last_time:
                try:
                    last_time = last1
                except:
                    last_time = ct - datetime.timedelta(hours=1)
            if str(last_time) == 'None': last_time = ct - datetime.timedelta(hours=1)
            if debounce is None:
                db_time = ct
            else:
                db_time = last_time + datetime.timedelta(seconds=debounce)
#                print('input debouncing ', ct, db_time)
            if ct >= db_time:
                locklist[device] = ct

            for trigger in results2:
                szenen = []
                latchMerker = False
                payloads = []
                kondition = []
                
                violTime = trigger.violTime
                latched = None                    
                
                single = True
#                    dicti = {}
#                    for i in range (0,len(row)):
#                        dicti[field_names[i]] = row[i]
                
                dicti = trigger.get_as_dict()
                if trigger.debug:
                    print(dicti)
                    
                descri = dicti.get("Status")
                if descri is None:
                    descri = ''                        
                    
                doppelklick = dicti.get("Doppelklick")
                if ct >= db_time and trigger.enabled and str(trigger.enabled) == "True":
                    # Hysteres einberechnen
                    lt = None
                    if not dicti['Value_lt'] is None and dicti['Value_lt'] != '':
                        lt = float(re_calc(dicti['Value_lt']))
                        if hyst is not None and str(dicti.get('latching')) == "True" and str(dicti.get('latched')) == "True":
                            lt = lt + float(hyst)
                    gt = None
                    if not dicti['Value_gt'] is None and dicti['Value_gt'] != '':
                        gt = float(re_calc(dicti['Value_gt']))
                        if hyst is not None and str(dicti.get('latching')) == "True" and str(dicti.get('latched')) == "True":
                            gt = gt - float(hyst)
                    eq = None
                    if not dicti['Value_eq'] is None and dicti['Value_eq'] != '':
                        eq = float(re_calc(dicti['Value_eq']))
                    append = True
                    if (lt is not None and lt <= value):
                        append = False
                    if (eq is not None and eq != value):
                        append = False                            
                    if (gt is not None and gt >= value):
                        append = False
                    if append and persTimer and dicti.get('violTime') is None: 
                        # Bedingungen sind erfüllt aber die Funktion wurde getimed ausgelöst, Peristtime, aber in der Zwischenzeit wurde schon resettiert
                        append = False
                        return None
#                        if append and (((lt or eq or gt) and 'Vm1' not in trigger.HKS) or 'XS1.V01' in trigger.Name):
#                            print(lt,eq,gt,value, type(dicti['Value_eq']), not dicti['Value_eq'] is None and dicti['Value_eq'] != '', re_calc(dicti['Value_eq'])) 
                    if trigger.debug:
                        print(lt,eq,gt,value)                            
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
                    if str(dicti.get('latching')) == "True":
                        if dicti.get('persistance') is None:
                            dicti['persistance'] = 0
                    if append and (dicti.get('violTime') is None or dicti.get('persistance') is None): # bedinung ist erfüllt und ViolTime war nicht gesetzt (set)
                        violTime = ct
                        # hier können wir dann den timer starten, oder besser dort wo wir auch wissen, das pesistence gibt
                    if not append and not dicti.get('violTime') is None: # bedingung nicht erfüllt und ViolTime war gesetzt (reset)
                        violTime = None
                    # hier war bisher nur append, das heisst aber das wir latchen, auch wenn nichts auszuführen ist.
                    # jetzt latchen wir nur, wenn auch eine Szene ausgeführt wird... mal schauen
                    # jetzt machen wir es auswählbar
                    if append and (szenen or trigger.latch_always):
                        latchMerker = True
                    if append and dicti.get('persistance') is not None:  # wir hätten was auszufühern aber persistence ist grösser null
                        if type(dicti.get('persistance')) == str and len(dicti.get('persistance')) == 0:
                            dicti['persistance'] = 0
                        if dicti.get('violTime') is not None:  # Zeit der ersten Bedinungsverletzung ist eingetragen
                            if ct - dicti.get("violTime") < datetime.timedelta(seconds=int(dicti.get('persistance'))): # persistence zeit ist noch nicht abgelaufen
                                szenen = []
                                payloads = []
                                kondition = []
                                latchMerker = False
                        if dicti.get('violTime') is None and datetime.timedelta(seconds=int(dicti.get('persistance'))) > datetime.timedelta(seconds=0):
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
                            latched = True

                    if trigger.debug:
                        print(append)                        
                    elem = InputsDatabase.get_element_by_id(dicti.get('Id'))
                    if append:
                        if elem:
                            elem.last2= elem.last1
                            elem.last1 = ct

                    if elem:
                        elem.violTime = violTime 
                        if latched:
                            elem.latched  = latched

                if trigger.debug:
                    print(szenen, payloads, kondition) 
                alle_szenen += szenen       
                alle_payloads += payloads
                descriptions += kondition                     

            if results2 and results2[0].Logging and str(hks) != str(device) and writeToInflx and not persTimer:
                thread_inflx = Timer(0, writeInfluxDb, [hks, value, utc])
                thread_inflx.start()


            if str(hks) != str(device) and add_to_mqtt:
                data = {"Value":value, "HKS":hks}
                mqtt_pub("Inputs/" + str(hks), data)
                mqtt_pub("Inputs/HKS/" + str(hks), data)
    if not filtered and not persTimer:
        prozessspiegel[hks] = value
#            results2 = [item for key, item in inputs_table_c.items() if item['Name'] == device]
    if not heartbt is None and not fallingback and not persTimer:
        if device in validTimers:
            validTimers[device]['timer'].cancel()
            if trigger_0.debug:
                print(validTimers[device]['timer'], 'canceled')
        entry = {'hks' : hks, 'desc' : desc, 'device':device, 'fallback':trigger_0.fallback}
        entry['due'] = datetime.datetime.now() + datetime.timedelta(0,int(heartbt))
        thread_pt_ = Timer(int(heartbt), invalidTimers, [device, desc])
        thread_pt_.start()
        entry['timer'] = thread_pt_
        validTimers[device] = entry
        if trigger_0.debug:
            print(entry)
        with open('hrtbt_timer.jsn', 'w') as fout:
            json.dump(validTimers, fout, default=json_serial) 
    if not trigger_0.Sturm_anz is None and  not trigger_0.Sturm_dauer is None and not persTimer:
        if hks in sturmTimers:
            sturmTimers[hks]['timer'].cancel()
        entry = {'hks' : hks, 'desc' : desc, 'device':device, 'Sturm':trigger_0.Sturm}
        entry['due'] = datetime.datetime.now() + datetime.timedelta(0,int(trigger_0.Sturm_dauer))
        thread_pt_ = Timer(int(trigger_0.Sturm_dauer), resetSturm, [trigger_0])
        thread_pt_.start()
        entry['timer'] = thread_pt_
        sturmTimers[hks] = entry            
#            print(validTimers.keys())

#    print('Time spend on inputs: ', str(datetime.datetime.now() - ct))
    if persTimer:
        for idx, szene in enumerate(alle_szenen):
            payload = {'Szene':szene, 'desc':descriptions[idx]}
            toolbox.communication.send_message(payload, typ='ExecSzene')              
    return alle_szenen, descriptions, heartbt, alle_payloads

#print(read_inputs_to_inputs_table())
server = None

def apptask():
#    global server
    app.run(host='0.0.0.0', port=4444)
#    server = Process(target=app.run)
#    server.start()
# ...
  
    
def main(): 
#    apptimer = Timer(0, apptask)
#    apptimer.start()  
#    app.run(host='0.0.0.0', port=4444)
    server = Process(target=apptask)
    server.start()   
    print('database server started goin into loop')
    while constants.run:
        time.sleep(1)
    
#    with open('inputs_table.jsn', 'w') as fout:
#        json.dump(InputsDB.get_as_list(), fout, default=json_serial) 
    InputsDatabase.save_to_file()
    SzenenDatabase.save_to_file()
    print("table written")
    server.terminate()
    server.join()  
    print('flask stopped')
    for key, timer in validTimers.items():
        try:
            timer['timer'].cancel()
        except Exception as e:
            pass
    for key, timer in sturmTimers.items():
        try:
            timer['timer'].cancel()
        except Exception as e:
            pass    
    # todo alle persistence timer noch stoppen
