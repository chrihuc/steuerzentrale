# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 13:15:11 2016

@author: christoph
"""

import constants

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from mysql_con import settings_r, mdb_get_table, re_calc, mdb_set_table

import easygui

app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree

from cmd_szenen import szenen

szn = szenen()
szn_lst = sorted(szn.list_commands('alle'))

class Szenen_tree():
    def __init__(self):
        self.p = None
        self.name = None
        self.inputs = mdb_get_table(db='cmd_inputs')
        self.set_paratree()
        
    def set_paratree(self):
        global p, name
        #szenen = mdb_get_table(db='set_Szenen')
        params = []
        inp_dict = {'name': u'Eingänge', 'type': 'group', 'expanded': True}
        inp_kinder = []
        for aktuator in self.inputs:   
            if aktuator.get('Description') <> None:
                title = aktuator.get('Description')
                akt_dict = {'name': aktuator.get('Input'), 'title':title , 'type': 'group', 'expanded': False}
                kinder1 = []
                kinder2 = []
                kinder3 = []
                for sub in sorted(aktuator):
                    if sub in ['Logging','Setting']:
                        if aktuator.get(sub) == '1':
                            kinder1.append({'name': sub, 'type': 'bool', 'value':True})
                        elif aktuator.get(sub) in ['0', None]:
                            kinder1.append({'name': sub, 'type': 'bool', 'value':False}) 
                        else:
                            kinder1.append({'name': sub, 'type': 'bool', 'value':aktuator.get(sub)}) 
                    if sub in ['Value_lt','Value_eq','Value_gt']:
                        kinder2.append({'name': sub, 'type': 'str', 'value':aktuator.get(sub)})
                    if sub in ['Wach','Schlafen','Schlummern','Leise','AmGehen','Gegangen','Abwesend','Urlaub','Besuch','Doppel','Dreifach']:
                        kinder3.append({'name': sub, 'type': 'list','value': aktuator.get(sub), 'values':szn_lst})    
                kinder = kinder1 + kinder2 + kinder3
                akt_dict['children'] = kinder
                inp_kinder.append(akt_dict)
        inp_dict['children'] = inp_kinder
        params.append(inp_dict)
        self.p = Parameter.create(name='params', type='group', children=params)

#params = [
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
#    ]}]
#p = Parameter.create(name='params', type='group', children=params)

t = ParameterTree()
sz=Szenen_tree()
#print sz
t.setParameters(sz.p, showTop=False)
t.setWindowTitle('Szenen Setup:')
#t2 = ParameterTree()
#t2.setParameters(p, showTop=False)

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)
layout.addWidget(t, 20, 0, 1, 1)
#layout.addWidget(t2, 1, 1, 1, 1)
win.show()
win.resize(800,800)

            
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
                