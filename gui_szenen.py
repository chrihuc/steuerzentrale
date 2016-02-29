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
from mysql_con import settings_r, mdb_read_table_entry, re_calc, mdb_set_table

import easygui

app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV
from cmd_satellites import satelliten
from cmd_szenen import szenen

from gui_inp import SzenenTreeInputs

xs1 = myezcontrol(constants.xs1_.IP)
hue = hue_lights()
sn = sonos()
tv = TV()
sat = satelliten()
xs1_devs = xs1.list_devices()
xs1_cmds = xs1.dict_commands()
hue_devs = hue.list_devices()
hue_cmds = hue.dict_commands()
sns_devs = sn.list_devices()
sns_cmds = sn.dict_commands()
tvs_devs = tv.list_devices()
tvs_cmds = tv.dict_commands()
sat_devs = sat.list_devices()
sat_cmds = sat.dict_commands()
cmd_devs = xs1_devs + hue_devs + sns_devs + tvs_devs + sat_devs

szn = szenen()
szn_lst = sorted(szn.list_commands('alle'))

szenen_beschreibung = mdb_read_table_entry(db='set_Szenen',entry='Description')

#==============================================================================
# Todo:
#   all list to be updated (no need to use dicts)
#   gehe zu szenen
#==============================================================================


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
        for seting in settings_r():
            opts['addList'].append(seting)
        #opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)
    
    def addNew(self, typ):
        values = settings_r()
        val=values.get(typ)
        self.addChild(dict(name=typ, type="str", value=val, removable=True, renamable=True))

class StockRaum():
    def __init__(self,name,zimmer = True):
        self.name = name
        self.dicti = {'name': 'Zimmer', 'type': 'group', 'expanded': False}
        self.children = []
        self.namen = {'Vm1':'Keller','V00':'Erdgeschoss','WOH':'Wohnzimer'}
        for nam in self.namen:
            if zimmer:
                if nam in self.name[-3:]:
                    self.dicti['name'] = self.namen.get(nam)   
            else:
                if nam in self.name[0:3]:
                    self.dicti['name'] = self.namen.get(nam)                     
        
    def addChild(self,child):
        global children
        self.children.append(child)

    def expand(self, status=True):
        self.dicti['expanded'] = status

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
    def __init__(self, Szene_to_read):
        self.szene_to_read = Szene_to_read
        self.p = None
        self.name = None
        self.szenen = [mdb_read_table_entry(db='set_Szenen',entry=self.szene_to_read)]
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
        if device in xs1_devs: values = xs1_cmds
        if device in hue_devs: values = hue_cmds
        if device in sns_devs: values = sns_cmds
        if device in tvs_devs: values = tvs_cmds
        if device in sat_devs: values = sat_cmds
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
        for stock in stock_list:
            stockwerke.append(StockRaum(stock))
        for zim in zimmer_list:
            zimmer.append(StockRaum(zim))            
        params = []
        for szene in self.szenen:
            szn_dict = {}
            if str(szene.get('Beschreibung')) <> 'None':
                self.name = szene.get('Beschreibung')
            else:
                self.name = 'Szenen Name: '+szene.get('Name')
            szn_dict['name'] = self.name
            szn_dict['type']='group'
            szn_dict['expanded'] = True
            szn_l_child = []
            ug_child = {'name': 'Untergeschoss', 'type': 'group', 'expanded': False}
            ug_zim1_child = {'name': 'Raum 1', 'type': 'group', 'expanded': False}
            ug_zim1_child_l = []
            
            eg_child = {'name': 'Erdgeschoss', 'type': 'group', 'expanded': False}
            eg_wohnzi_child = {'name': 'Wohnzimmer', 'type': 'group', 'expanded': False}
            eg_wohnzi_child_l = []
            eg_kueche_child = {'name': u'Küche', 'type': 'group', 'expanded': False}
            eg_kueche_child_l = []   
            eg_flur_child = {'name': u'Flur', 'type': 'group', 'expanded': False}
            eg_flur_child_l = []     
            
            og_child = {'name': '1. Stock', 'type': 'group', 'expanded': False}
            og_sch_child = {'name': 'Schlafzimmer', 'type': 'group', 'expanded': False}
            og_sch_child_l = []
            og_bad_child = {'name': 'Bad', 'type': 'group', 'expanded': False}
            og_bad_child_l = []            
            
            dg_child = {'name': 'Dach', 'type': 'group', 'expanded': False}

            
            szn_sn_child = {'name': 'Sonos Devices', 'type': 'group', 'expanded': False}
            szn_sn_child_l = []              
            del szene['Name']
            for item in szene:
                szn_d_child = {}
                szn_d_child_l = []
                if str(item) in cmd_devs:
                    zwname = szenen_beschreibung.get(item)
                    if zwname <> None:
                        kom_group = KommandoGroup(name=str(item), title = zwname,cmds=self.get_commando_set(str(item)), children=self.dict_constructor_(str(item),self.__return_enum__(szene.get(item))))
                for zim in zimmer:
                    if zim.name in str(item):
                        zim.addChild(kom_group)
                        if kom_group.shouldExpand():
                            zim.expand(True)
                            #Stockwerke auch expandieren
                if 'V00WOH' in str(item):
                    eg_wohnzi_child_l.append(kom_group)
                    if kom_group.shouldExpand():
                        eg_wohnzi_child['expanded']= True
                        eg_child['expanded']= True
                elif 'V00KUE' in str(item):               
                    eg_kueche_child_l.append(kom_group)
                    if kom_group.shouldExpand():
                        eg_kueche_child['expanded']= True 
                        eg_child['expanded']= True
                elif 'V00FLU' in str(item):               
                    eg_flur_child_l.append(kom_group)
                    if kom_group.shouldExpand():
                        eg_flur_child['expanded']= True 
                        eg_child['expanded']= True         
                elif 'Vm1ZIM' in str(item):               
                    ug_zim1_child_l.append(kom_group)
                    if kom_group.shouldExpand():
                        ug_zim1_child['expanded']= True 
                        ug_child['expanded']= True                            
                elif 'V01SCH' in str(item):               
                    og_sch_child_l.append(kom_group)
                    if kom_group.shouldExpand():
                        og_sch_child['expanded']= True 
                        og_child['expanded']= True                                     
                elif str(item) in ['Setting']: 
                    for child in self.__return_enum__(szene.get(item)):
                        if type(self.__return_enum__(szene.get(item))) == dict:
                            szn_d_child_l.append({'name': child, 'type': 'str', 'value': self.__return_enum__(szene.get(item)).get(child)})
                    szn_d_child = ScalableGroup(name= item, children= szn_d_child_l, expanded = False) 
                    szn_l_child.append(szn_d_child) 
                elif str(item) in ['Bedingung']: 
                    szn_d_child = {'name': item, 'type': 'action', 'expanded': False} 
                    kinder = self.__return_enum__(szene.get(item))
                    for child in kinder:
                        if type(kinder) == dict:
                            szn_d_child_l.append({'name': 'Bedingung %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'Setting', 'type': 'str', 'value': child},
                        {'name': 'Operand', 'type': 'str', 'value': '='},{'name': 'Bedingung', 'type': 'str', 'value': kinder.get(child)}],'tip': "This is a checkbox"})
                        else:
                            if child <> None:
                                szn_d_child_l.append({'name': 'Bedingung %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'Setting', 'type': 'str', 'value': child[0]},
                        {'name': 'Operand', 'type': 'str', 'value': child[1]},{'name': 'Bedingung', 'type': 'str', 'value': child[2]}],'tip': "This is a checkbox"})
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)                             
                elif str(item) in ['setTask']: 
                    szn_d_child = {'name': 'Befehl an Handys', 'type': 'action', 'expanded': False} 
                    kinder = self.__return_enum__(szene.get(item))  
                    for kind in kinder:       
                        if kind <> None:
                            szn_d_child_l.append({'name': 'Befehl %d' % (len(szn_d_child_l)+1), 'type': 'group', 'children':[{'name': 'An wen', 'type': 'str', 'value': kind[0]},
                        {'name': 'Befehl', 'type': 'str', 'value': kind[1]}]})  
                    szn_d_child['children']= szn_d_child_l
                    szn_l_child.append(szn_d_child)                             
                elif str(item) in ['Follows']: 
                    szn_d_child = {'name': 'Szene folgt', 'type': 'action', 'expanded': False} 
                    kinder = self.__return_enum__(szene.get(item))  
                    for kind in kinder:       
                        if kind <> None:
                            szn_d_child_l.append({'name': 'Szene %d' % (len(szn_d_child_l)+1), 'type': 'action', 'children':[{'name': 'Szene', 'type': 'list','value': kind[0], 'values':szn_lst},
                        {'name': 'nach [s]', 'type': 'float', 'value': kind[1]},{'name': u'Verlängerbar', 'type': 'int', 'value': kind[2]}]})  
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
                    if str(item) in ['Prio','Delay__']:
                        szn_d_child['type'] = 'float'
                        szn_d_child['step'] = 0.1
                    else:
                        szn_d_child['type'] = 'str'
                    szn_d_child['expanded'] = False
                    if str(szene.get(item)) <> "None":
                        szn_d_child['value'] = str(szene.get(item))
                    else:
                        szn_d_child['value'] = ''
                    szn_l_child.append(szn_d_child)
                #if int(szene.get('Id')) >6: break
                eg_wohnzi_child['children']= eg_wohnzi_child_l
                eg_kueche_child['children']= eg_kueche_child_l
                eg_flur_child['children']= eg_flur_child_l
                og_sch_child['children']= og_sch_child_l

            ug_child_l = [ug_zim1_child]
            ug_child['children'] = ug_child_l
            szn_l_child.append(ug_child)   
          
            eg_child_l = [eg_wohnzi_child, eg_kueche_child, eg_flur_child]
            eg_child['children'] = eg_child_l
            szn_l_child.append(eg_child)    
            
            og_child_l = [og_sch_child]
            og_child['children'] = og_child_l
            szn_l_child.append(og_child)             

      
            szn_dict['children']= szn_l_child
            params.append(szn_dict)
        szn_dict =     {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
                {'name': 'Speichere Szene', 'type': 'action'},
                {'name': u'Prüfe Bedingung', 'type': 'action'},
                {'name': 'Execute', 'type': 'action'}
                
            ]}
        params.append(szn_dict)   
        self.p = Parameter.create(name='params', type='group', children=params)
        self.p.param('Save/Restore functionality', 'Speichere Szene').sigActivated.connect(self.save)
        self.p.param('Save/Restore functionality', u'Prüfe Bedingung').sigActivated.connect(self.check_bedingung)
        self.p.param('Save/Restore functionality', 'Execute').sigActivated.connect(self.execute)
        self.p.param(self.name, 'Befehl an Handys').sigActivated.connect(self.add_task)
        self.p.param(self.name, 'Bedingung').sigActivated.connect(self.add_bedingung)
        self.p.param(self.name, 'Szene folgt').sigActivated.connect(self.addSzene)
        self.linkSzene()
        return params

    def add_setting(self):
        global p
        self.p.param(self.name, 'Setting').addChild({'name': '', 'type': 'str', 'value': ''})

    def add_bedingung(self):
        global p
        self.p.param(self.name, 'Bedingung').addChild({'name': 'Bedingung ','type': 'group', 'children':[{'name': 'Setting', 'type': 'str', 'value': ''},
                        {'name': 'Operand', 'type': 'str', 'value': ''},{'name': 'Bedingung', 'type': 'str', 'value': ''}]}, autoIncrementName=True)

    def add_task(self):
        global p
        self.p.param(self.name, 'Befehl an Handys').addChild({'name': 'Befehl ','type': 'group', 'children':[{'name': 'An wen', 'type': 'str', 'value': ''},
                        {'name': 'Befehl', 'type': 'str', 'value': ''}]}, autoIncrementName=True)

    def addSzene(self):
        global p
        self.p.param(self.name, 'Szene folgt').addChild({'name': 'Befehl ', 'type': 'action', 'children':[{'name': 'Szene', 'type': 'list','value': '', 'values':szn_lst},
                        {'name': 'nach [s]', 'type': 'float', 'value': 0},{'name': u'Verlängerbar', 'type': 'int', 'value': 2}]}, autoIncrementName=True)

    def linkSzene(self):
        for kind in self.p.param(self.name, 'Szene folgt').children():
            kind.sigActivated.connect(self.makeInit(kind.getValues().get('Szene')[0]))
            
    def makeInit(self, Name):
        def setInit(): 
            self.__init__(Name) 
        return setInit
            
#params1 = [
#    {'name': 'Basic parameter data types', 'type': 'group', 'children': [
#        {'name': 'Integer', 'type': 'int', 'value': 10},
#        {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
#        {'name': 'String', 'type': 'str', 'value': "hi"},
#        {'name': 'List', 'type': 'list', 'values': [1,2,3], 'value': 2},
#        {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3,3,3]}, 'value': 0},
#        {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
#        {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
#        {'name': 'Gradient', 'type': 'colormap'},
#        {'name': 'Subgroup', 'type': 'group', 'children': [
#            {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
#            {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
#        ]},
#        {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
#        {'name': 'Action Parameter', 'type': 'action'},
#    ]},
#    {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
#        {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True, 'suffix': 'V'},
#        {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
#        {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True, 'suffix': 'Hz'},
#        
#    ]},
#    {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
#        {'name': 'Save State', 'type': 'action'},
#        {'name': 'Restore State', 'type': 'action', 'children': [
#            {'name': 'Add missing items', 'type': 'bool', 'value': True},
#            {'name': 'Remove extra items', 'type': 'bool', 'value': True},
#        ]},
#    ]},
#    {'name': 'Extra Parameter Options', 'type': 'group', 'children': [
#        {'name': 'Read-only', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
#        {'name': 'Renamable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
#        {'name': 'Removable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'removable': True},
#    ]},
#    ComplexParameter(name='Custom parameter group (reciprocal values)'),
#    ScalableGroup(name="Expandable Parameter Group", children=[
#        {'name': 'ScalableParam 1', 'type': 'str', 'value': "default param 1"},
#        {'name': 'ScalableParam 2', 'type': 'str', 'value': "default param 2"},
#    ]),
#]

## Create tree of Parameter objects


## If anything changes in the tree, print a message
#def change(param, changes):
#    print("tree changes:")
#    for param, change, data in changes:
#        path = p.childPath(param)
#        if path is not None:
#            childName = '.'.join(path)
#        else:
#            childName = param.name()
#        print('  parameter: %s'% childName)
#        print('  change:    %s'% change)
#        print('  data:      %s'% str(data))
#        print('  ----------')
#        print param.getValues().items()
#        print param.value()
#    
##p.sigTreeStateChanged.connect(change)
#
#
#def valueChanging(param, value):
#    return    
#    print("Value changing (not finalized):", param, value)
    
# Too lazy for recursion:
#for child in p.children():
#    child.sigValueChanging.connect(valueChanging)
#    for ch2 in child.children():
#        ch2.sigValueChanging.connect(valueChanging)
        
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
                                    set_dict[some_object.get('children').get(sub).get('name')]  = some_object.get('children').get(sub).get('value')
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
                            if only_change:
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
                                    set_lst.append([szn_tuple.get('Szene').get('value'), szn_tuple.get('nach [s]').get('value'), szn_tuple.get(u'Verlängerbar').get('value')])
                            dicti['Follows'] = set_lst                             
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
                            dicti.update(self.itera(some_object.get(item)))
    #        except Exception,e:
    #            print e
        return dicti

    def save(self):
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)
        print neu_szene
        mdb_set_table(table='set_Szenen', device=self.szene_to_read, commands=neu_szene)
            

    def check_bedingung(self):
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state, False)
        bedingungen = neu_szene.get('Bedingung')
        for i, wert in enumerate(bedingungen):
            for j, eintrag in enumerate(wert):
                bedingungen[i][j]=re_calc(eintrag)
        efuellt = szn.__bedingung__(bedingungen,verbose=True)
#        if efuellt:
#            easygui.msgbox("Szene würde ausgeführt", title="Bedingung Check")
#        else:
#            easygui.msgbox("Szene würde NICHT ausgeführt", title="Bedingung Check")

    def execute(self):
        constants.redundancy_.master = True
        if szn.execute(self.szene_to_read):
            pass            
            #easygui.msgbox("Szene ausgeführt", title="Execute")
        else:
            easygui.msgbox("Szene wurde NICHT ausgeführt", title="Execute")
        constants.redundancy_.master = False            

def selected(text):
    global sz, t
    sz=Szenen_tree(text)
    t.setParameters(sz.p, showTop=False)
    print text

#==============================================================================
#Uncomment following block to use as class 
#
#==============================================================================


#comboBox.activated[str].connect(self.style_choice)
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
        if path[-1] in ['Wach','Schlafen','Schlummern','Leise','AmGehen','Gegangen','Abwesend','Urlaub','Besuch','Doppel','Dreifach']:
            selected(str(data))
    



t = ParameterTree()
sz=Szenen_tree("Alles_ein")
inp=SzenenTreeInputs()
t.setParameters(sz.p, showTop=False)
t.setWindowTitle('Szenen Setup:')
t2 = ParameterTree()
t2.setParameters(inp.p, showTop=False)

inp.p.sigTreeStateChanged.connect(change)

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
comboBox = QtGui.QComboBox(win)
for szne in szn_lst:
    comboBox.addItem(szne)
comboBox.setMaxVisibleItems(50)    
comboBox.activated[str].connect(selected)
layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)
layout.addWidget(t, 2, 1, 1, 1)
layout.addWidget(comboBox, 1, 1, 1, 1)
layout.addWidget(t2, 2, 0, 1, 1)
win.show()
win.resize(800,800)

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
        QtGui.QApplication.instance().exec_()
    