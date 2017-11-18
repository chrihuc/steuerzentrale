# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 07:13:57 2016

@author: christoph
"""

# -*- coding: utf-8 -*-
"""
This example demonstrates the use of pyqtgraph's parametertree system. This provides
a simple way to generate user interfaces that control sets of parameters. The example
demonstrates a variety of different parameter types (int, float, list, etc.)
as well as some customized parameter types

"""

import constants

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
#from mysql_con import settings_r, setting_s, mdb_read_table_entry, re_calc, mdb_set_table, mdb_get_table,getSzenenSources, maxSzenenId, mdb_read_table_column, mdb_add_table_entry
from database import mysql_connector
from database import mysql_connector as msqc

import easygui
import socket

app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from outputs import sonos
from outputs import xs1
from outputs import hue
from outputs import samsung
from outputs import satellites
from outputs import szenen
import timeit

#from gui_inp import SzenenTreeInputs

xs1 = xs1.XS1(constants.xs1_.IP)
hue = hue.Hue_lights()
sn = sonos.Sonos()
tv = samsung.TV()
sat = satellites.Satellite()
szn = szenen.Szenen()
#xs1_devs = xs1.list_devices()
xs1_cmds = xs1.dict_commands()
#hue_devs = hue.list_devices()
hue_cmds = hue.dict_commands()
#sns_devs = sn.list_devices()
sns_cmds = sn.dict_commands()
#tvs_devs = tv.list_devices()
tvs_cmds = tv.dict_commands()
#sat_devs = sat.list_devices()
sat_cmds = sat.dict_commands()
devices_types = mysql_connector.mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
TYPES = ['XS1','SATELLITE','ZWave', 'SONOS', 'HUE', 'TV']
cmd_devs = [device for device in devices_types if devices_types[device] in TYPES]
szn_lst = sorted(szn.list_commands(gruppe=''))
#for cmd_set in [xs1_cmds,hue_cmds,sns_cmds,tvs_cmds,sat_cmds]:
#    cmd_set.update({'warte_1':len(cmd_set)+1,'warte_3':len(cmd_set)+2,'warte_5':len(cmd_set)+3})

cmd_lsts = ['out_hue','out_Sonos']
cmd_lsts += sat.listCommandTable('alle',nameReturn = False)
cmd_lsts = list(set(cmd_lsts))

szn_typs = ['','Favorit', 'GUI','Intern','Scanner','Wecker','Lichter','Klima', 'Multimedia']
stockwerke = ['Vm1','V00','A00','V01','V02','VIR','']

stockwerke_dict = {'Vm1':'Keller','V00':'Erdgeschoss','V01':'1. Stock','V02':'2. Stock',
                   'A00':'Draussen', 'VIR':'Virtuell', 'NEW':'Unassigned'}

zim_dict = {'ZIM':'Zimmer',
            'WOH':'Wohnzimmer',
            'KUE':u'Küche',
            'BAD':u'Badezimmer/Toilette',
            'SCH':'Schlafzimmer',
            'FLU':'Flur',
            'BUE':u'Büro',
            'KID':'Kinderzimmer',
            'ESS':'Esszimmer',
            'TER':'Terasse',
            'GEN':'Generell',

            'KOM':'Kommunikation',
            'BEW':'Bewohner'}

furn_dict = {'SCA':'Scanner',
             'ADV':'Advent',
             'EIN':'Eingang',
             'STV':'Stromversorgung',
             'RUM':'Raum',
             'DEK':'Decke',
             'SRA':'Schrank',
             'SOF':'Sofa',
             'TUE':u'Tür',
             'SEV':'Server',
             'PFL':'Pflanzen',
             'BET':'Bett',
             'TER':'Terasse',
             'GEN':'Generell',

             'SSH':'SecureShell',
             'RUT':'Router',
             'SAT':'Satellite',
             'USB':'USBKey',
             'IPA':'Handy'}


szenen_beschreibung = mysql_connector.mdb_read_table_entry(db='set_Szenen',entry='Description')
constants.redundancy_.master = True

#==============================================================================
# TODO:
#   all list to be updated (no need to use dicts)
#   gehe zu szenen
#   codes mit listen ersetzen
#   save settings not working
#==============================================================================

start = timeit.default_timer()

# tree setup
tree_szenen = ParameterTree()
tree_inputs_devices = ParameterTree()
tree_input_device = ParameterTree()
tree_dvc_tp_cmds = ParameterTree()
tree_settings = ParameterTree()

# other init
lastSelected = ''

## test subclassing parameters
## This parameter automatically generates two child parameters which are always reciprocals of each other
class ComplexParameter(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'bool'
        opts['value'] = True
        pTypes.GroupParameter.__init__(self, **opts)

        self.addChild({'name': 'A = 1/B', 'type': 'float', 'value': 7, 'suffix': 'Hz', 'siPrefix': True})
        self.addChild({'name': 'B = 1/A', 'type': 'float', 'value': 1/7., 'suffix': 's', 'siPrefix': True})
        self.a = self.param('A = 1/B')
        self.b = self.param('B = 1/A')
        self.a.sigValueChanged.connect(self.aChanged)
        self.b.sigValueChanged.connect(self.bChanged)

    def aChanged(self):
        self.b.setValue(1.0 / self.a.value(), blockSignal=self.bChanged)

    def bChanged(self):
        self.a.setValue(1.0 / self.b.value(), blockSignal=self.aChanged)


## test add/remove
## this group includes a menu allowing the user to add new parameters into its child list
class ScalableGroup(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        opts['addList'] = []
        for seting in mysql_connector.settings_r():
            opts['addList'].append(seting)
        #opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self, typ):
        values = mysql_connector.settings_r()
        val=values.get(typ)
        self.addChild(dict(name=typ, type="str", value=val, removable=True, renamable=True))

class StockRaum():
    def __init__(self,name,zimmer = True):
        self.name = name
        self.dicti = {'name': 'Zimmer', 'type': 'group', 'expanded': False}
        self.dicti['name'] = self.get_description(name)
        print name, self.dicti['name']
        self.children = []
        self.expanded = False
#        self.namen = {'Vm1':'Keller','V00':'Erdgeschoss','V01':'1. Stock','V02':'2. Stock','A00':'Draussen',
#                      'TER':'Terasse','GRA':'Gras',
#                      'ZIM':'Zimmer','WOH':'Wohnzimer','KUE':u'Küche','BAD':u'Badezimmer/Toilette','SCH':'Schlafzimmer','FLU':'Flur','BUE':u'Büro','ESS':'Esszimmer',
#                      'SCA':'Scanner','ADV':'Advent','KID':'Kinderzimmer','EIN':'Eingang','STV':'Stromversorgung'}
#        for nam in self.namen:
#            if zimmer:
#                if nam in self.name[-3:]:
#                    self.dicti['name'] = self.get_description(nam)
#            else:
#                if nam in self.name[0:3]:
#                    self.dicti['name'] = self.get_description(nam)

    @staticmethod
    def get_description(obj_id):
        dictionaries = [stockwerke_dict, zim_dict, furn_dict]
        if len(obj_id) > 3:
            obj_id = obj_id[-3:]
        for dicit in dictionaries:
            if obj_id in dicit:
                return dicit[obj_id]

    def addChild(self,child):
        self.children.append(child)

    def expand(self, status=True):
        self.dicti['expanded'] = status
        self.expanded = status

    def build(self):
        self.dicti['children'] = self.children
        return self.dicti

class KommandoGroup(pTypes.GroupParameter):
    def __init__(self, cmds, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        opts['addList'] = ['list']
        opts['expanded'] = False
        self.cmds = cmds
        pTypes.GroupParameter.__init__(self, **opts)
        self.autoExpand()

    def addNew(self, typ):
        val = {
            'list': self.cmds
        }[typ]
        self.addChild(dict(name="Kommando %d" % (len(self.childs)+1), type=typ, values=self.cmds, value=val, removable=True, renamable=True))

    def shouldExpand(self):
        for kind in self.children():
            if kind.value() > 1:
                return True
        else:
            return False

    def autoExpand(self):
        for kind in self.children():
            if kind.value() > 1:
                self.setOpts(expanded = True)
        else:
            return False

class Szenen_tree():

    szenen = []
    neue_szene = False

    def __init__(self, Szene_to_read):
        self.szene_to_read = Szene_to_read
        self.p = None
        self.name = None
        # self.szenen = [mdb_read_table_entry(db='set_Szenen',entry=self.szene_to_read,recalc=False)]
        # self.set_paratree()

    def __return_enum__(self,eingabe):
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

    def update(self, neue_szene):
        self.szene_to_read = neue_szene
        self.szenen = [mysql_connector.mdb_read_table_entry(db='set_Szenen',entry=self.szene_to_read,recalc=False)]
        self.set_paratree()

    def dict_constructor(self,name, values, value):
        if str(name) == "None": name = ''
        dicti = {'name':name, 'type':'list','values':values}
        for val in values:
            if str(val) == str(value):
                dicti['value'] = values.get(val)
        return dicti

    def group_constructor(self,name, namen, values, values2):
        if str(name) == "None": name = ''
        dicti = {'name':name, 'type':'group', 'expanded': True}
        liste = []
        itera = 0
        for value in values2:
            try:
                name = namen[itera]
            except:
                name = "Kommando " + str(itera+1)
            liste.append(self.dict_constructor(name, values, value))
            itera += 1
        dicti['children']= liste
        return dicti

    def get_commando_set(self,device):
        if devices_types[device] == 'XS1': values = xs1_cmds
        if devices_types[device] == 'HUE': values = hue_cmds
        if devices_types[device] == 'SONOS': values = sns_cmds
        if devices_types[device] == 'TV': values = tvs_cmds
        if devices_types[device] in ['SATELLITE', 'ZWave']: values = sat.dict_commands(device)
        values.update({'warte_1':len(values)+1,'warte_3':len(values)+2,'warte_5':len(values)+3})
        return values

    def dict_constructor_(self,device, cmmds):
        liste = []
        itera  = 1
        for cmd in (cmmds):
            dicti = {}
            values = self.get_commando_set(device)
            dicti = {'name':'Kommando ' + str(itera), 'type':'list','values':values}
            itera += 1
            for val in values:
                if str(val) == str(cmd):
                    dicti['value'] = values.get(val)
                    if values.get(val) == 1:
                        dicti['expanded'] = False
            liste.append(dicti)
        return liste

    def getValueFromValues(self,value, values):
        for num, val in enumerate(values):
            if str(val) == str(value):
                print val, num
                return num + 1

    def set_paratree(self):
        global p, name
        #szenen = mdb_get_table(db='set_Szenen')
        tipps = mysql_connector.mdb_read_table_entry(db='set_Szenen',entry='Description')
        stock_list = []
        stockwerke = []
        zimmer_list = []
        zimmer = []
        for szene in self.szenen:
            for item in szene:
                if str(item) in cmd_devs:
                    name = str(item)
                    stock_list.append(name[0:3])
                    zimmer_list.append(name[0:6])
        stock_list = list(set(stock_list))
        zimmer_list = list(set(zimmer_list))
        print stock_list, zimmer_list
        for stock in stock_list:
            stockwerke.append(StockRaum(stock))
        for zim in zimmer_list:
            zimmer.append(StockRaum(zim))
        params = []
        for szene in self.szenen:
            if szene.get('Name') == 'LeereVorlage' or self.neue_szene:
                szene['Name']= 'NeueSzene'
                szene['Id'] = mysql_connector.maxSzenenId()-mysql_connector.maxSzenenId()%10 +10
                self.neue_szene = False
            szn_dict = {}
            if str(szene.get('Beschreibung')) <> 'None':
                self.name = szene.get('Beschreibung')
            else:
                self.name = 'Szenen Name: '+str(szene.get('Name'))
            szn_dict['name'] = self.name
            szn_dict['type']='group'
            szn_dict['expanded'] = True
            szn_l_child = []
            #del szene['Name']
            for item in szene:
                szn_d_child = {}
                szn_d_child_l = []
                if str(item) in cmd_devs:
                    zwname = szenen_beschreibung.get(item)
                    if zwname == None:
                        zwname = str(item)
                    kom_group = KommandoGroup(name=str(item), title = zwname,cmds=self.get_commando_set(str(item)), children=self.dict_constructor_(str(item),self.__return_enum__(szene.get(item))))
                    for zim in zimmer:
                        if zim.name in str(item):
                            zim.addChild(kom_group)
                            if kom_group.shouldExpand():
                                zim.expand(True)
                                #Stockwerke auch expandieren
                elif str(item) in ['Setting']:
                    for child in self.__return_enum__(szene.get(item)):
                        if type(self.__return_enum__(szene.get(item))) == dict:
                            szn_d_child_l.append({'name': child, 'type': 'str', 'value': self.__return_enum__(szene.get(item)).get(child)})
                    szn_d_child = ScalableGroup(name= item, children= szn_d_child_l, expanded = False)
                    szn_l_child.append(szn_d_child)
                elif str(item) in ['Bedingung']:
                    szn_d_child = {'name': item, 'type': 'action', 'expanded': True}
                    kinder = self.__return_enum__(szene.get(item))
                    for child in kinder:
                        if type(kinder) == dict:
                            szn_d_child_l.append({'name': 'Bedingung %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'Setting', 'type': 'str', 'value': child},
                        {'name': 'Operand', 'type': 'list', 'values':['==','=','<','>','<=','>=','in','!'], 'value': '='},{'name': 'Bedingung', 'type': 'str', 'value': kinder.get(child)}],'tip': "This is a checkbox"})
                        else:
                            if child <> None:
                                szn_d_child_l.append({'name': 'Bedingung %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'Setting', 'type': 'list','values':['']+sorted(mysql_connector.settings_r()), 'value': child[0]},
                        {'name': 'Operand', 'type': 'list', 'values':['==','=','<','>','<=','>=','in','!'],'value': child[1]},{'name': 'Bedingung', 'type': 'str', 'value': child[2]}]})
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)
                elif str(item) in ['setTask']:
                    szn_d_child = {'name': 'Befehl an Handys', 'type': 'action', 'expanded': True}
                    kinder = self.__return_enum__(szene.get(item))
                    for kind in kinder:
                        if kind <> None:
                            szn_d_child_l.append({'name': 'Befehl %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'An wen', 'type': 'str', 'value': kind[0]},
                        {'name': 'Befehl', 'type': 'str', 'value': kind[1]}]})
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)
                elif str(item) in ['Follows']:
                    szn_d_child = {'name': 'Szene folgt', 'type': 'action', 'expanded': True}
                    kinder = self.__return_enum__(szene.get(item))
                    for kind in kinder:
                        if kind <> None:
                            if len(kind)<4:
                                immer = True
                            else:
                                immer = kind[3]
                            if len(kind)<5:
                                depErfolg = 0
                            else:
                                depErfolg = kind[4]
                            szn_d_child_l.append({'name': 'Szene %d' % (len(szn_d_child_l)+1), 'type': 'action', 'children':[{'name': 'Szene', 'type': 'list','value': kind[0], 'values':szn_lst},
                        {'name': 'nach [s]', 'type': 'str', 'value': kind[1]},{'name': 'Verlaengerbar', 'type': 'list', 'values':{'Verlaengerbar':0,'nur exact':1,'fest':2}, 'value': kind[2]},{'name': 'Abhaengig Bedingung', 'type': 'bool', 'value': immer}
                        ,{'name': 'Abhaengig Erfolg', 'type': 'list', 'values':{'egal':0,'bei Erfolg':1,'bei Nichterfolg':2}, 'value': depErfolg}]})
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)
                elif str(item) in ['Cancels']:
                    szn_d_child = {'name': 'Folgende stoppen', 'type': 'action', 'expanded': True}
                    kinder = self.__return_enum__(szene.get(item))
                    for kind in kinder:
                        if kind <> None:
                            szn_d_child_l.append({'name': 'Stops %d' % (len(szn_d_child_l)+1), 'type': 'list','value': kind, 'values':szn_lst})
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)
                elif str(item) in ['AutoMode']:
                    szn_d_child['name'] = str(item)
                    szn_d_child['type'] = 'bool'
                    szn_d_child['expanded'] = False
                    if str(szene.get(item)) <> "None":
                        szn_d_child['value'] = eval(szene.get(item))
                    else:
                        szn_d_child['value'] = False
                    szn_l_child.append(szn_d_child)
                else:
                    szn_d_child['name'] = str(item)
                    if str(item) in ['Delay']:
                        szn_d_child['type'] = 'float'
                        szn_d_child['step'] = 0.1
                        if str(szene.get(item)) <> "None":
                            szn_d_child['value'] = float(szene.get(item))
                        else:
                            szn_d_child['value'] = None
                    elif str(item) in ['Prio']:
                        szn_d_child['type'] ='list'
                        szn_d_child['values'] = {'Kein Event':-1,'Normales Event':0,'Problem ohne Hinweis':1,'Hinweis wenn zuhause':2,'immer Hinweis':3,'Hinweis wenn wach':4,
                                                 'Achtung wenn wach':5,'Alarm':6,'Debug':7}
                        if str(szene.get(item)) <> "None":
                            szn_d_child['value'] = float(szene.get(item))
                    elif str(item) in ['Gruppe']:
                        szn_d_child['type'] ='list'
                        szn_d_child['values'] = szn_typs
                        if str(szene.get(item)) <> "None":
                            szn_d_child['value'] = str(szene.get(item))
                        else:
                            szn_d_child['value'] = ''
                    else:
                        szn_d_child['type'] = 'str'
                        if str(szene.get(item)) <> "None":
                            szn_d_child['value'] = str(szene.get(item))
                        else:
                            szn_d_child['value'] = ''
                        try:
                            if tipps[str(item)] <> None:
                                szn_d_child['tip'] = str(tipps[str(item)])
                        except:
                            pass
                    szn_d_child['expanded'] = False
                    szn_l_child.append(szn_d_child)

            for stock in stockwerke:
                for zim in zimmer:
                    if stock.name in zim.name:
                        stock.addChild(zim.build())
                        if zim.expanded:
                            stock.expand(True)
                szn_l_child.append(stock.build())
            szn_dict['children']= szn_l_child
            params.append(szn_dict)
        ichilds, schilds = [], []
        iquellen, squellen = mysql_connector.getSzenenSources(self.szene_to_read)
        for quelle in iquellen:
            ichilds.append({'name': quelle.get('Name'), 'type': 'action', 'value': quelle.get('Name'),'autoIncrementName':True})
        for quelle in squellen:
            schilds.append({'name': quelle.get('Name'), 'type': 'action', 'value': quelle.get('Name'),'autoIncrementName':True})
        szn_dict = {'name': 'Sources', 'type': 'group', 'children': [
                {'name': 'Inputs', 'type': 'group', 'autoIncrementName':True, 'children':ichilds },
                {'name': 'Szenen', 'type': 'group', 'autoIncrementName':True, 'children':schilds }
            ]}
        params.append(szn_dict)
        szn_dict =     {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
                {'name': 'Speichere Szene', 'type': 'action'},
                {'name': u'Prüfe Bedingung', 'type': 'action'},
                {'name': 'Execute', 'type': 'action'},
                {'name': 'Execute on server', 'type': 'action'},
                {'name': 'Neue Szene', 'type': 'action'},
                {'name': 'Dupliziere Szene', 'type': 'action'}
            ]}
        params.append(szn_dict)
        self.p = Parameter.create(name='params', type='group', children=params)
        try:
            self.p.param('Save/Restore functionality', 'Speichere Szene').sigActivated.connect(self.save)
            self.p.param('Save/Restore functionality', u'Prüfe Bedingung').sigActivated.connect(self.check_bedingung)
            self.p.param('Save/Restore functionality', 'Execute').sigActivated.connect(self.execute)
            self.p.param('Save/Restore functionality', 'Execute on server').sigActivated.connect(self.execute_on_server)
            #self.p.param('Save/Restore functionality', 'Neue Szene').sigActivated.connect(self.newSzene)
            self.p.param(self.name, 'Befehl an Handys').sigActivated.connect(self.add_task)
            self.p.param(self.name, 'Bedingung').sigActivated.connect(self.add_bedingung)
            self.p.param(self.name, 'Szene folgt').sigActivated.connect(self.addSzene)
            self.p.param(self.name, 'Folgende stoppen').sigActivated.connect(self.addCancels)
            self.linkSzene()
        except:
            pass
        return params

    def add_setting(self):
        global p
        self.p.param(self.name, 'Setting').addChild({'name': '', 'type': 'str', 'value': ''})

    def add_bedingung(self):
        global p
        self.p.param(self.name, 'Bedingung').addChild({'name': 'Bedingung ','type': 'group', 'children':[{'name': 'Setting', 'type': 'list','values':sorted(mysql_connector.settings_r()), 'value': ''},
                        {'name': 'Operand', 'type': 'list', 'values':['==','=','<','>','<=','>=','in','!'], 'value': ''},{'name': 'Bedingung', 'type': 'str', 'value': ''}]}, autoIncrementName=True)

    def add_task(self):
        global p
        self.p.param(self.name, 'Befehl an Handys').addChild({'name': 'Befehl ','type': 'group', 'children':[{'name': 'An wen', 'type': 'str', 'value': ''},
                        {'name': 'Befehl', 'type': 'str', 'value': ''}]}, autoIncrementName=True)

    def addSzene(self):
        global p
        self.p.param(self.name, 'Szene folgt').addChild({'name': 'Befehl ', 'type': 'action', 'children':[{'name': 'Szene', 'type': 'list','value': '', 'values':szn_lst},
                        {'name': 'nach [s]', 'type': 'float', 'value': 0},{'name': 'Verlaengerbar', 'type': 'list', 'values':{'Verlaengerbar':0,'nur exact':1,'fest':2}, 'value': 0},{'name': 'Abhaengig Bedingung', 'type': 'bool', 'value': True}
                        ,{'name': 'Abhaengig Erfolg', 'type': 'list', 'values':{'egal':0,'bei Erfolg':1,'bei Nichterfolg':2}, 'value': 0}]}, autoIncrementName=True)

    def addCancels(self):
        global p
        self.p.param(self.name, 'Folgende stoppen').addChild({'name': 'Szene', 'type': 'list','value': '', 'values':szn_lst}, autoIncrementName=True)

    def linkSzene(self):
        for kind in self.p.param(self.name, 'Szene folgt').children():
            kind.sigActivated.connect(self.makeInit(kind.getValues().get('Szene')[0]))

    def makeInit(self, Name):
        def setInit():
            self.__init__(Name)
        return setInit


    def check_iter(self,some_object):
        try:
            iter(some_object)
            if type(some_object) <> str:
                return True
            else:
                return False
        except TypeError, te:
            return False

    def return_list(self,some_object):
        liste = []
        for item in some_object:
            dicti = some_object.get(item)
            sub_dicti = dicti.get('values')
            wert = dicti.get('value')
            if sub_dicti <> None:
                for jtem in sub_dicti:
                    if sub_dicti[jtem] == wert:
                        wert_str = jtem
                if wert_str <> '':
                    liste.append(wert_str)
        if len(liste) > 0:
            return liste
        else:
            return None


    def itera(self,some_object, only_change = False):
        dicti = {}
        h_dict = {}
        if self.check_iter(some_object):
            if True:
            #try:
                if type(some_object) == list: print some_object
                if some_object.get('type') == 'group' or some_object.get('type') == 'action':
                    device  = some_object.get('name')
                    if device in self.szenen[0]:
                        if device in ['Setting']:
                            set_dict = {}
                            for sub in some_object.get('children'):
                                if some_object.get('children').get(sub).get('value') <> '':
                                    try:
                                        set_dict[some_object.get('children').get(sub).get('name')]  = eval(some_object.get('children').get(sub).get('value'))
                                    except:
                                        set_dict[some_object.get('children').get(sub).get('name')]  = (some_object.get('children').get(sub).get('value'))
                            dicti[device] = set_dict
                        elif device in ['Bedingung']:
                            set_lst = []
                            for child in some_object.get('children'):
                                bed_tuple = some_object.get('children').get(child).get('children')
                                if bed_tuple.get('Setting').get('value') <> '':
                                    #check if list:
                                    try:
                                        set_lst.append([bed_tuple.get('Setting').get('value'), bed_tuple.get('Operand').get('value'), eval(bed_tuple.get('Bedingung').get('value'))])
                                    except:
                                        set_lst.append([bed_tuple.get('Setting').get('value'), bed_tuple.get('Operand').get('value'), (bed_tuple.get('Bedingung').get('value'))])
                            dicti[device] = set_lst
                        else:
                            kommandos = self.return_list(some_object.get('children'))
                            if str(device) == "Id":
                                dicti[device] = kommandos
                            elif only_change:
                                if self.szenen[0].get(device) <> kommandos:
                                    dicti[device] = kommandos
                            else:
                                dicti[device] = kommandos
                    else:
                        if device == 'Befehl an Handys':
                            set_lst = []
                            for child in some_object.get('children'):
                                tsk_tuple = some_object.get('children').get(child).get('children')
                                if tsk_tuple.get('An wen').get('value') <> '':
                                    set_lst.append([tsk_tuple.get('An wen').get('value'), tsk_tuple.get('Befehl').get('value')])
                            dicti['setTask'] = set_lst
                        elif device == 'Szene folgt':
                            set_lst = []
                            for child in some_object.get('children'):
                                szn_tuple = some_object.get('children').get(child).get('children')
                                if szn_tuple.get('Szene').get('value') <> '':
                                    print szn_tuple.get('Verlaengerbar')
                                    set_lst.append([szn_tuple.get('Szene').get('value'), szn_tuple.get('nach [s]').get('value'), szn_tuple.get('Verlaengerbar').get('value'),
                                                    szn_tuple.get('Abhaengig Bedingung').get('value'),szn_tuple.get('Abhaengig Erfolg').get('value')])
                            dicti['Follows'] = set_lst
                        elif device == 'Folgende stoppen':
                            set_lst = []
                            for child in some_object.get('children'):
                                if some_object.get('children').get(child).get('value') <> '':
                                    szen = some_object.get('children').get(child).get('value')
                                    set_lst.append(szen)
                            dicti['Cancels'] = set_lst
                        else:
                            #strucutre group only if name not ambivalent
                            dicti.update(self.itera(some_object.get('children')))
                else:
                    if some_object.get('name') <> None:
                        if some_object.get('name') in self.szenen[0]:
                            device  = some_object.get('name')
                            value = some_object.get('value')
                            if value == '': value = None
                            if only_change:
                                if self.szenen[0].get(device) <> value:
                                    dicti[some_object.get('name')] =  value
                            else:
                                dicti[some_object.get('name')] =  value
                    else:
                        #ordered dict:
                        for item in some_object:
                            if some_object.get(item).get('name') <> 'Sources':
                                dicti.update(self.itera(some_object.get(item)))
    #        except Exception,e:
    #            print e
        return dicti

    def save(self):
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)
        print neu_szene
        mysql_connector.mdb_set_table(table='set_Szenen', device=neu_szene.get('Id'), commands=neu_szene, primary = 'Id')


    def check_bedingung(self):
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state, False)
        bedingungen = neu_szene.get('Bedingung')
        for i, wert in enumerate(bedingungen):
            for j, eintrag in enumerate(wert):
                bedingungen[i][j]=mysql_connector.re_calc(eintrag)
        efuellt = szn.__bedingung__(bedingungen,verbose=True)
        if efuellt:
            easygui.msgbox("Szene würde ausgeführt", title="Bedingung Check")
        else:
            easygui.msgbox("Szene würde NICHT ausgeführt", title="Bedingung Check")

    def execute(self):
        constants.redundancy_.master = True
        if szn.execute(self.szene_to_read):
            pass
            #easygui.msgbox("Szene ausgeführt", title="Execute")
        else:
            easygui.msgbox("Szene wurde NICHT ausgeführt", title="Execute")
        #constants.redundancy_.master = False

    def execute_on_server(self):
        commado = {'Szene':str(self.szene_to_read)}
        csocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        csocket.sendto(str(commado),(constants.udp_.SERVER,constants.udp_.broadPORT))

    def newSzene(self):
        global szenen
        self.szenen = [mysql_connector.mdb_read_table_entry(db='LeereVorlage',entry=self.szene_to_read)]
        self.set_paratree()

class InputsTree():
    def __init__(self, expand = None, isInputs = True, inputsGroup = None, cmdTable = None):
        self.p = None
        self.name = None
        self.expand = expand
        self._szn_lst = sorted(szn.list_commands(gruppe="alle"))
        if isInputs:
            self.inputs = mysql_connector.mdb_get_table(db='cmd_inputs')
        else:
            self.inputs = mysql_connector.mdb_get_table(db=cmdTable)
        if inputsGroup == None:
            self.inputsGroup = ''
        else:
            self.inputsGroup = inputsGroup
        self.eingaenge = []
        for inpu in self.inputs:
            self.eingaenge.append(str(inpu.get('Id')))
        self.isInputs = isInputs
#        if not cmdTable is None:
#            cmdTable = sorted(cmdTable)
        self.cmdTable = cmdTable
        self.set_paratree()

    def set_paratree(self):
        params = []
        if self.isInputs:
            inp_dict = {'name': u'Eingänge', 'type': 'group', 'expanded': True}
        else:
            inp_dict = {'name': u'Befehle', 'type': 'group', 'expanded': True}
        inp_kinder = []
        for aktuator in sorted(self.inputs):
            if (aktuator.get('Description') <> None and self.inputsGroup in aktuator.get('Name') and self.isInputs) or (not self.isInputs and not aktuator.get('Name') in ['Name']):
                if self.isInputs:
                    title = aktuator.get('Description')
                else:
                    title = str(aktuator.get('Name'))
                akt_dict = {'name': str(aktuator.get('Id')), 'title':title , 'type': 'group', 'expanded': False}
                if self.expand == aktuator.get('Name'):
                    akt_dict['expanded']= True
                kinder1 = []
                kinder2 = []
                kinder3, kinder4 = [], []
                for sub in sorted(aktuator):
                    if sub in ['Logging','Setting','Doppelklick']:
                        if aktuator.get(sub) == '1':
                            kinder1.append({'name': sub, 'type': 'bool', 'value':True})
                        elif aktuator.get(sub) in ['0', None]:
                            kinder1.append({'name': sub, 'type': 'bool', 'value':False})
                        else:
                            kinder1.append({'name': sub, 'type': 'bool', 'value':eval(aktuator.get(sub))})
                    elif sub in ['Description']:
                        kinder2.append({'name': sub, 'title':'Beschreibung', 'type': 'str', 'value':aktuator.get(sub)})
                    elif sub in ['Value_lt','Value_eq','Value_gt']:
                        kinder3.append({'name': sub, 'type': 'str', 'value':aktuator.get(sub)})
                    elif sub in ['Immer','Wach','Wecken','Schlafen','Schlummern','Leise','AmGehen','Gegangen','Abwesend','Urlaub','Besuch','Doppel','Dreifach']:
                        kinder4.append({'name': sub, 'type': 'list','value': aktuator.get(sub), 'values':self._szn_lst})
                    elif sub in ['Id']:
                        pass
                    else:
                        kinder2.append({'name': sub, 'type': 'str', 'value':aktuator.get(sub)})
                kinder = kinder1 + kinder2 + kinder3 + kinder4
                akt_dict['children'] = kinder
                inp_kinder.append(akt_dict)
        inp_dict['children'] = inp_kinder
        params.append(inp_dict)
        if self.isInputs:
            inp_dict = {'name': 'Aktionen', 'type': 'group', 'children': [
                    {'name': 'Speichere Inputs', 'type': 'action'}
                ]}
            params.append(inp_dict)
        else:
            inp_dict = {'name': 'Aktionen', 'type': 'group', 'children': [
                    {'name': 'Speichere', 'type': 'action'},
                    {'name': 'Neues Kommando', 'type': 'action'}
                ]}
            params.append(inp_dict)
        self.p = Parameter.create(name='params', type='group', children=params)
        if self.isInputs:
            self.p.param('Aktionen', 'Speichere Inputs').sigActivated.connect(self.save)
        else:
            self.p.param('Aktionen', 'Speichere').sigActivated.connect(self.save)
            self.p.param('Aktionen', 'Neues Kommando').sigActivated.connect(self.newCommand)

    def save(self):
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)

    def newCommand(self):
        mysql_connector.mdb_add_table_entry(table=self.cmdTable, values={'Name':'Neuer Befehl'})
        self.set_paratree()

    def check_iter(self,some_object):
        try:
            iter(some_object)
            if type(some_object) <> str:
                return True
            else:
                return False
        except TypeError, te:
            return False

    def itera(self,some_object):
        dicti = {}
        if self.check_iter(some_object):
            if some_object.get('type') == 'group':
                eingang = some_object.get('name')
                if eingang in self.eingaenge and eingang <> None:
                    for aktuator in self.inputs:
                        if str(aktuator.get('Id')) == str(eingang):
                            for kind in some_object.get('children'):
                                wert = some_object.get('children').get(kind).get('value')
                                if wert == '': wert = None
                                if wert <> aktuator.get(kind):
                                    dicti[kind] = wert
                            if self.isInputs:
                                mysql_connector.mdb_set_table(table=constants.sql_tables.inputs.name, device=str(aktuator.get('Id')), commands=dicti, primary = 'Id')
                            elif len(dicti) > 0:
                                mysql_connector.mdb_set_table(table=self.cmdTable, device=str(aktuator.get('Id')), commands=dicti, primary = 'Id', translate = False)
                else:
                    self.itera(some_object.get('children'))
            else:
                for item in some_object:
                    self.itera(some_object.get(item))

"""
part with new devices tree
"""

class TreeInputsDevices(object):
    def __init__(self, callback=None):
        self.cb = callback
        #self.inputs = mdb_get_table(db='cmd_inputs')
        self.params = []
#        self.set_paratree(inputs)

    def add_sub_object(self, top_object, sub_object_Id, expanded=False):
        name = None
        if sub_object_Id[:3] in furn_dict:
            expanded=False
        for liste in [stockwerke_dict, zim_dict, furn_dict]:
            if sub_object_Id[:3] in liste:
                name = liste[sub_object_Id[:3]]
                break

        sub_object = {'title': name, 'type': 'group', 'expanded': expanded,
                             'name':sub_object_Id, 'children':[]}
        top_object['children'].append(sub_object)
        return sub_object

    def get_sub_object(self, top_object, sub_object_Id):
        for obj in top_object['children']:
            if obj['name'] == sub_object_Id:
                return obj
        return self.add_sub_object(top_object, sub_object_Id)

    def add_device(self, top_object, device):
        device_id = device['Id']
        if device['Status'] is None:
            stat = ''
        else:
            stat = device['Status']
        device_desc = device['Description'] + ' ' + stat
        dev_obj = {'title': device['HKS'], 'type': 'group', 'expanded': True,
                   'name':str(device_id), 'children':[], 'tip':device_desc}
        kind = {'title': device['HKS'], 'type': 'str', 'expanded': True,
                'name':'Beschreibung', 'value':device_desc}
        dev_obj['children'].append(kind)
        kind = {'title': device['HKS'], 'type': 'action', 'expanded': True,
                'name':str(device_id), 'value':device_desc}
        dev_obj['children'].append(kind)
        top_object['children'].append(dev_obj)

    def set_paratree(self, inputs):
        # top level floors
        top_level = {'name': u'Eingänge', 'type': 'group', 'expanded': True, 'children':[]}
#        for floor in stockwerke_dict:
#            floor_obj = {'name': stockwerke_dict[floor], 'type': 'group', 'expanded': True,
#                         'Id':floor}
#            top_level['children'].append(floor_obj)
        for aktuator in sorted(inputs):
            aktuator_hks = aktuator['HKS']
            if aktuator_hks is not None:
                level = aktuator_hks[:3]
                if level in stockwerke:
                    level_obj = self.get_sub_object(top_level, level)
                    raum = aktuator_hks[3:7]
                    raum_obj = self.get_sub_object(level_obj, raum)
                    furni = aktuator_hks[7:11]
                    furni_obj = self.get_sub_object(raum_obj, furni)
                    device = aktuator_hks[11:]
                    self.add_device(furni_obj, aktuator)
                else:
                    level = 'NEW'
                    level_obj = self.get_sub_object(top_level, level)
                    if aktuator['Description'] != None and aktuator['Description'] != '':
                        self.add_device(level_obj, aktuator)
        self.params = Parameter.create(name='params', type='group', children=[top_level])
        self.walk_param(self.params)

    def walk_param(self, obj):
        if obj.isType('group'):
            for kid in obj.children():
                self.walk_param(kid)
        elif obj.isType('action'):
            obj.sigActivated.connect(self.printit(obj.name()))

    def printit(self, value):
        def print_wrapper():
            self.cb(value)
        return print_wrapper

class TreeInputDevice(object):
    def __init__(self):
        self.params = []
        self._inputs = None
#        self.set_paratree(device)

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    def set_paratree(self, device_id):
        for device in self.inputs:
            if str(device['Id']) == str(device_id):
                break
        top_level = {'name': str(device['Id']), 'type': 'group', 'expanded': True, 'children':[]}
        kinder = top_level['children']
        kinder.insert(0, {'name':'Description', 'title':'Beschreibung', 'type': 'str',
                                  'value':device['Description']})
        kinder.insert(1, {'name':'Status', 'title':'Status', 'type': 'str',
                                  'value':device['Status']})
        for feature, value in device.iteritems():
            if feature in ['Logging','Setting','Doppelklick']:
                kinder.insert(2, {'name':feature, 'type': 'bool', 'value':eval(value)})
            elif feature in ['Immer', 'Wach', 'Wecken', 'Schlafen', 'Schlummern', 'Leise',
                             'AmGehen', 'Gegangen', 'Abwesend', 'Urlaub', 'Besuch', 'Doppel',
                             'Dreifach']:
                kinder.append({'name':feature, 'type': 'list', 'value':value,
                               'values':sorted(szn_lst)})
            elif feature in ['Id', 'Description', 'Status']:
                pass
            else:
                kinder.insert(2, {'name':feature, 'type': 'str', 'value':value})
        top_level_list = [top_level]
        action = {'name': 'Speichern', 'type': 'action'}
        top_level_list.append(action)
        action = {'name': 'Loeschen', 'type': 'action'}
        top_level_list.append(action)
        self.params = Parameter.create(name='params', type='group', children=top_level_list)
        self.params.child('Speichern').sigActivated.connect(self.speichern)
        self.params.child('Loeschen').sigActivated.connect(self.loeschen)

    def speichern(self):
        szene = {}
        print "doing"
        for kind in self.params.children():
            if kind.isType('group'):
                szene['Id'] = kind.name()
                for enkel in kind.children():
                    if enkel.value() != '':
                        szene[enkel.name()] = enkel.value()
                    else:
                        szene[enkel.name()] = None
        print szene
        mysql_connector.mdb_set_table(table=constants.sql_tables.inputs.name, device=str(szene.get('Id')),
                      commands=szene, primary = 'Id', translate = False)

    def loeschen(self):
        for kind in self.params.children():
            if kind.isType('group'):
                _id = kind.name()
        mysql_connector.remove_entry(table=constants.sql_tables.inputs.name, device=_id,
                                     primary = 'Id')

"""
old part
"""
sets = []

class SettingsTree():
    def __init__(self, isInputs = True, cmdTable = None):
        self.p = None
        self.name = None
        self.set_paratree()

    def __return_enum__(self,eingabe):
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

    def set_paratree(self):
        params = []
        dicti = {'name': u'Settings', 'type': 'group', 'expanded': True}
        kinder = []
        for seti in sets:
            kind = {'name':seti.get('Name')}
            if seti.get('Typ') == None:
                kind['type'] = 'str'
                kind['value'] = seti.get('Value')
            elif '[' in seti.get('Typ'):
                kind['type'] = 'list'
                kind['values']=self.__return_enum__(seti.get('Typ'))
                kind['value']  = seti.get('Value')
            else:
                kind['type'] =seti.get('Typ')
                kind['value']  = eval(seti.get('Value'))
            kinder.append(kind)
        dicti['children'] = kinder
        inp_dict = {'name': 'Aktionen', 'type': 'group', 'children': [
                {'name': 'Speichern', 'type': 'action'},
                {'name': 'Speichern2', 'type': 'action'}
            ]}
        params.append(dicti)
        params.append(inp_dict)
        self.p = Parameter.create(name='params', type='group', children=params)
        self.p.param('Aktionen', 'Speichern').sigActivated.connect(self.set_speichern)
        self.p.param('Aktionen', 'Speichern2').sigActivated.connect(self.printit)

    def set_speichern(self):
        print "here"
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)

    def printit(self):
        print "yup"

    def check_iter(self,some_object):
        try:
            iter(some_object)
            if type(some_object) <> str:
                return True
            else:
                return False
        except TypeError, te:
            return False

    def itera(self,some_object, only_change = False):
        dicti = {}
        if self.check_iter(some_object):
            if some_object.get('type') == 'group':
                seting = some_object.get('name')
                print seting
                if seting <> None:
                    for seti in sets:
                        for kind in some_object.get('children').get('Settings').get('children'):
                            wert = some_object.get('children').get('Settings').get('children').get(kind).get('value')
                            if wert == '': wert = None
                            dicti[kind] = wert
                    for setting in dicti:
                        print setting,dicti.get(setting)
                        mysql_connector.setting_s(setting,dicti.get(setting))
                else:
                    self.itera(some_object.get('children'))
            else:
                for item in some_object:
                    self.itera(some_object.get(item))

sz=Szenen_tree('')
def print_vale(value):
    print value

def populate_input_tree_1():
    ipts = mysql_connector.mdb_get_table(db='cmd_inputs')
    tree_ipt_devices.set_paratree(ipts)
    tree_inputs_devices.setParameters(tree_ipt_devices.params, showTop=False)
    tree_ipt_devices.params.sigStateChanged.connect(change)

def populate_input_tree_2(szene=''):
    ipts = mysql_connector.mdb_get_table(db='cmd_inputs')
    tree_ipt_dev_vals.inputs = ipts
    tree_ipt_dev_vals.set_paratree(szene)
    tree_input_device.setParameters(tree_ipt_dev_vals.params, showTop=False)

def populate_dvcs_cmds_tree():
    cmds=InputsTree(isInputs = False, cmdTable = (cmd_lsts[0]))
    tree_dvc_tp_cmds.setParameters(cmds.p, showTop=False)

def populate_settngs_tree():
    seTre = SettingsTree()
    tree_settings.setParameters(seTre.p, showTop=False)

def selected(text):
    global lastSelected
    lastSelected = text
    sz.update(lastSelected)
    print 'selected'
    tree_szenen.setParameters(sz.p, showTop=False)
    sz.p.sigTreeStateChanged.connect(change_sz)

def update_device_lists():
    global szn_lst, xs1_devs, xs1_cmds, hue_devs, hue_cmds, sns_devs, sns_cmds, tvs_devs
    global tvs_cmds, sat_devs, sat_cmds, cmd_devs
    szn_lst = sorted(szn.list_commands(gruppe=''))
    xs1_devs = msqc.tables.akt_type_dict['XS1']
    xs1_cmds = xs1.dict_commands()
    hue_devs = msqc.tables.akt_type_dict['HUE']
    hue_cmds = hue.dict_commands()
    sns_devs = msqc.tables.akt_type_dict['SONOS']
    sns_cmds = sn.dict_commands()
    tvs_devs = msqc.tables.akt_type_dict['TV']
    tvs_cmds = tv.dict_commands()
    sat_devs = msqc.tables.akt_type_dict['SATELLITE']
    sat_devs += msqc.tables.akt_type_dict['ZWave']
    sat_cmds = sat.dict_commands()
    cmd_devs = xs1_devs + hue_devs + sns_devs + tvs_devs + sat_devs

def update_settings():
    global sets
    sets = mysql_connector.mdb_get_table(constants.sql_tables.settings.name)

def update():
    update_settings()
    update_device_lists()
    selected(lastSelected)
    populate_input_tree_1()
    populate_input_tree_2()
    populate_dvcs_cmds_tree()
    populate_settngs_tree()
    updt_sznlst()

    cBox_dvc_tp_cmds.clear()
    for cmdLst in cmd_lsts:
        cBox_dvc_tp_cmds.addItem(cmdLst)
    cBox_dvc_tp_cmds.activated[str].connect(slctCmdLst)
    cBox_inpts_new.clear()
    inpts = sorted(mysql_connector.mdb_read_table_column(db="cmd_inputs", column = 'Name'))
    for inpt in inpts:
        if str(inpt) <> "":
            cBox_inpts_new.addItem(str(inpt))
    sz.p.sigTreeStateChanged.connect(change_sz)

def neuTrig():
    vals = mysql_connector.mdb_read_table_entry(db="cmd_inputs",entry=str(cBox_inpts_new.currentText()),column='Name')
    vals2 = {value:vals[value] for value in vals if vals[value] is not None}
    mysql_connector.mdb_add_table_entry("cmd_inputs",vals2)

def change(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = inp.p.childPath(param)
        print path
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')
        if data <> '':
            if path[-1] in ['Wach','Schlafen','Schlummern','Leise','AmGehen','Gegangen','Abwesend','Urlaub','Besuch','Doppel','Dreifach']:
                selected(str(data))

def change_sz(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = sz.p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
            if param.parent().name() == 'Szene folgt':
                selected(param.child('Szene').value())
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')
        if data <> '':
            if path[-2] in ['Szenen']:
                selected(str(path[-1]))
#        if data <> '':
#            if path[-2] in ['Inputs']:
#                showInputs(str(path[-1]))
        if data <> '':
            if path[0] in ['Save/Restore functionality'] and path[1] == 'Neue Szene':
                selected('LeereVorlage')
            if path[0] in ['Save/Restore functionality'] and path[1] == 'Dupliziere Szene':
                sz.neue_szene = True
                selected(lastSelected)


def slctCmdLst(text):
    global cmds, tree_dvc_tp_cmds
    cmds=InputsTree(isInputs = False, cmdTable = text)
    tree_dvc_tp_cmds.setParameters(cmds.p, showTop=False)

def updt_sznlst():
    cBox_scenes.clear()
    szn_lst = sorted(szn.list_commands(str(cBox_scn_types.currentText())))
    for szne in szn_lst:
        cBox_scenes.addItem(szne)


tree_ipt_devices = TreeInputsDevices(callback=populate_input_tree_2)
tree_ipt_dev_vals = TreeInputDevice()

# setup window
win = QtGui.QWidget()


tree_w_szenes = ParameterTree()
#sz=Szenen_tree("Alles_ein")
inp=InputsTree(isInputs = True, inputsGroup = 'V00')
print timeit.default_timer() - start
            # 0.747

#t.setParameters(sz.p, showTop=False)
#t.setWindowTitle('Szenen Setup:')
tree_w_inputs = ParameterTree()
tree_select_input = ParameterTree()
print timeit.default_timer() - start
            # 0.7
#tree_w_inputs.setParameters(inp.p, showTop=False)
print timeit.default_timer() - start
            # 16.69

t3 = ParameterTree()
print timeit.default_timer() - start
cmds=InputsTree(isInputs = False, cmdTable = cmd_lsts[0])
#t3.setParameters(cmds.p, showTop=False)
print timeit.default_timer() - start
t4 = ParameterTree()
#seTre = SettingsTree()
#t4.setParameters(seTre.p, showTop=False)

print timeit.default_timer() - start
inp.p.sigTreeStateChanged.connect(change)


layout = QtGui.QGridLayout()
win.setLayout(layout)
win.showMaximized()

#inp=InputsTree(isInputs = True, inputsGroup = 'V00')
#cmds=InputsTree(isInputs = False, cmdTable = cmd_lsts[0])
#inp.p.sigTreeStateChanged.connect(change)

cBox_scenes = QtGui.QComboBox(win)
cBox_scenes.setMaxVisibleItems(50)
cBox_scenes.activated[str].connect(selected)

cBox_dvc_tp_cmds = QtGui.QComboBox(win)
cBox_inpts_new = QtGui.QComboBox(win)


cBox_scn_types = QtGui.QComboBox(win)
for itm in szn_typs:
    cBox_scn_types.addItem(itm)
cBox_scn_types.activated[str].connect(updt_sznlst)


cBox_Stockwerke = QtGui.QComboBox(win)
#for itm in stockwerke:
#    cBox_Stockwerke.addItem(itm)
#cBox_Stockwerke.setCurrentIndex(1)
#cBox_Stockwerke.activated[str].connect(updInputs)

print timeit.default_timer() - start
update()
#selected('Gehen')

buttn_update = QtGui.QPushButton(win)
buttn_update.setText('Update')
buttn_update.clicked.connect(update)

adinbttn = QtGui.QPushButton(win)
adinbttn.setText('Neuer Trigger')
adinbttn.clicked.connect(neuTrig)

layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)

# column 0
layout.addWidget(buttn_update, 1, 0, 1, 1)
layout.addWidget(cBox_Stockwerke, 2, 0, 1, 1)
layout.addWidget(tree_inputs_devices, 3, 0, 1, 1)
layout.addWidget(tree_input_device, 4, 0, 1, 1)
layout.addWidget(cBox_inpts_new, 5, 0, 1, 1)
layout.addWidget(adinbttn, 6, 0, 1, 1)

# column 1
#szene preselection

layout.addWidget(cBox_scn_types, 1, 1, 1, 1)
layout.addWidget(cBox_scenes, 2, 1, 1, 1)
layout.addWidget(tree_szenen, 3, 1, 2, 1)

# column 2
layout.addWidget(cBox_dvc_tp_cmds, 2, 2, 1, 1)
layout.addWidget(tree_dvc_tp_cmds, 3, 2, 2, 1)

# column 3
layout.addWidget(tree_settings, 3, 3, 2, 1)

win.setWindowTitle('Schalttafel')
win.show()
win.resize(1400,1200)
print timeit.default_timer() - start
#==============================================================================
# till here
#==============================================================================

# test save/restore
#s = p.saveState()
#p.restoreState(s)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication.instance()
        app.setWindowIcon(QtGui.QIcon('/home/christoph/spyder/sz/Control_Panel.png'))
        app.exec_()
#        QtGui.QApplication.instance().exec_()
