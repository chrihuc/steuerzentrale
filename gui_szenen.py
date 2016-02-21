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
from mysql_con import mdb_get_table, mdb_read_table_entry

app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV
from cmd_satellites import satelliten

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
        opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)
    
    def addNew(self, typ):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[typ]
        self.addChild(dict(name="ScalableParam %d" % (len(self.childs)+1), type=typ, value=val, removable=True, renamable=True))

def __return_enum__(eingabe):
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

def dict_constructor(name, values, value):
    if str(name) == "None": name = ''
    dicti = {'name':name, 'type':'list','values':values}
    for val in values:
        if str(val) == str(value):
            dicti['value'] = values.get(val)
    return dicti

def group_constructor(name, namen, values, values2):
    if str(name) == "None": name = ''
    dicti = {'name':name, 'type':'group', 'expanded': True}    
    liste = []
    itera = 0
    for value in values2:
        try:
            name = namen[itera]
        except:
            name = "Kommando " + str(itera+1)
        liste.append(dict_constructor(name, values, value))
        itera += 1
    dicti['children']= liste
    return dicti

#szenen = mdb_get_table(db='set_Szenen')
szenen = [mdb_read_table_entry(db='set_Szenen',entry='Alles_ein')]
params = []
for szene in szenen:
    if int(szene.get('Id')) >9:
        szn_dict = {}
        szn_dict['name']=szene.get('Name')
        szn_dict['type']='group'
        szn_dict['expanded'] = False
        szn_l_child = []
        szn_xs_child = {'name': 'XS1 Devices', 'type': 'group', 'expanded': False}
        szn_xs_child_l = []
        szn_hu_child = {'name': 'Hue Devices', 'type': 'group', 'expanded': False}
        szn_hu_child_l = []  
        szn_sn_child = {'name': 'Sonos Devices', 'type': 'group', 'expanded': False}
        szn_sn_child_l = []       
        szn_tv_child = {'name': 'TVs', 'type': 'group', 'expanded': False}
        szn_tv_child_l = []
        szn_sat_child = {'name': 'Satellites', 'type': 'group', 'expanded': False}
        szn_sat_child_l = []        
        del szene['Name']
        for item in szene:
            szn_d_child = {}
            if str(item) in xs1_devs:
                listeee =group_constructor(str(item), [], xs1_cmds, __return_enum__(szene.get(item)))
                szn_xs_child_l.append(listeee)
            elif str(item) in hue_devs:
                listeee =group_constructor(str(item), [], hue_devs, __return_enum__(szene.get(item)))                
                szn_hu_child_l.append(listeee)
            elif str(item) in sns_devs:
                szn_d_child['name'] = str(item)
                szn_d_child['type'] = 'list'
                szn_d_child['values'] = sns_cmds
                for cmd in sns_cmds:
                    szn_d_child['value']= 0
                    if cmd == str(szene.get(item)):
                        szn_d_child['value']= sns_cmds.get(cmd)   
                szn_sn_child_l.append(szn_d_child)
            elif str(item) in tvs_devs:
                szn_d_child['name'] = str(item)
                szn_d_child['type'] = 'list'
                szn_d_child['values'] = tvs_cmds
                for cmd in tvs_cmds:
                    szn_d_child['value']= 0
                    if cmd == str(szene.get(item)):
                        szn_d_child['value']= tvs_cmds.get(cmd)   
                szn_tv_child_l.append(szn_d_child)
            elif str(item) in sat_devs:
                szn_d_child['name'] = str(item)
                szn_d_child['type'] = 'list'
                szn_d_child['values'] = sat_cmds
                for cmd in sat_cmds:
                    szn_d_child['value']= 0
                    if cmd == str(szene.get(item)):
                        szn_d_child['value']= sat_cmds.get(cmd)   
                szn_sat_child_l.append(szn_d_child)                
            else:
                szn_d_child['name'] = str(item)
                szn_d_child['type'] = 'str'
                szn_d_child['expanded'] = False
                if str(szene.get(item)) <> "None":
                    szn_d_child['value'] = str(szene.get(item))
                else:
                    szn_d_child['value'] = ''
                szn_l_child.append(szn_d_child)
            #if int(szene.get('Id')) >6: break
            szn_xs_child['children']= szn_xs_child_l
            szn_hu_child['children']= szn_hu_child_l
            szn_sn_child['children']= szn_sn_child_l
            szn_tv_child['children']= szn_tv_child_l
            szn_sat_child['children']= szn_sat_child_l            
        szn_l_child.append(szn_xs_child)
        szn_l_child.append(szn_hu_child)
        szn_l_child.append(szn_sn_child)
        szn_l_child.append(szn_tv_child)
        szn_l_child.append(szn_sat_child)        
        szn_dict['children']= szn_l_child
        params.append(szn_dict)
szn_dict =     {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
        {'name': 'Save State', 'type': 'action'},
        {'name': 'Restore State', 'type': 'action', 'children': [
            {'name': 'Add missing items', 'type': 'bool', 'value': True},
            {'name': 'Remove extra items', 'type': 'bool', 'value': True},
        ]},
    ]}
params.append(szn_dict)    

params1 = [
    {'name': 'Basic parameter data types', 'type': 'group', 'children': [
        {'name': 'Integer', 'type': 'int', 'value': 10},
        {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
        {'name': 'String', 'type': 'str', 'value': "hi"},
        {'name': 'List', 'type': 'list', 'values': [1,2,3], 'value': 2},
        {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3,3,3]}, 'value': 0},
        {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
        {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
        {'name': 'Gradient', 'type': 'colormap'},
        {'name': 'Subgroup', 'type': 'group', 'children': [
            {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
            {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
        ]},
        {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
        {'name': 'Action Parameter', 'type': 'action'},
    ]},
    {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
        {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True, 'suffix': 'V'},
        {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
        {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True, 'suffix': 'Hz'},
        
    ]},
    {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
        {'name': 'Save State', 'type': 'action'},
        {'name': 'Restore State', 'type': 'action', 'children': [
            {'name': 'Add missing items', 'type': 'bool', 'value': True},
            {'name': 'Remove extra items', 'type': 'bool', 'value': True},
        ]},
    ]},
    {'name': 'Extra Parameter Options', 'type': 'group', 'children': [
        {'name': 'Read-only', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
        {'name': 'Renamable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
        {'name': 'Removable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'removable': True},
    ]},
    ComplexParameter(name='Custom parameter group (reciprocal values)'),
    ScalableGroup(name="Expandable Parameter Group", children=[
        {'name': 'ScalableParam 1', 'type': 'str', 'value': "default param 1"},
        {'name': 'ScalableParam 2', 'type': 'str', 'value': "default param 2"},
    ]),
]

## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)

## If anything changes in the tree, print a message
def change(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')
    
p.sigTreeStateChanged.connect(change)


def valueChanging(param, value):
    return    
    print("Value changing (not finalized):", param, value)
    
# Too lazy for recursion:
for child in p.children():
    child.sigValueChanging.connect(valueChanging)
    for ch2 in child.children():
        ch2.sigValueChanging.connect(valueChanging)
        


def save():
    global state
    state = p.saveState()
    
def restore():
    global state
    add = p['Save/Restore functionality', 'Restore State', 'Add missing items']
    rem = p['Save/Restore functionality', 'Restore State', 'Remove extra items']
    p.restoreState(state, addChildren=add, removeChildren=rem)
p.param('Save/Restore functionality', 'Save State').sigActivated.connect(save)
p.param('Save/Restore functionality', 'Restore State').sigActivated.connect(restore)


## Create two ParameterTree widgets, both accessing the same data
t = ParameterTree()
t.setParameters(p, showTop=False)
t.setWindowTitle('pyqtgraph example: Parameter Tree')
#t2 = ParameterTree()
#t2.setParameters(p, showTop=False)

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel("These are two views of the same data. They should always display the same values."), 0,  0, 1, 2)
layout.addWidget(t, 1, 0, 1, 1)
#layout.addWidget(t2, 1, 1, 1, 1)
win.show()
win.resize(800,800)

## test save/restore
#s = p.saveState()
#p.restoreState(s)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()