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

class SzenenTreeInputs():
    def __init__(self):
        self.p = None
        self.name = None
        self.inputs = mdb_get_table(db='cmd_inputs')
        self.eingaenge = []
        for inpu in self.inputs:
            self.eingaenge.append(inpu.get('Name'))
        self.set_paratree()
        
    def set_paratree(self):
        global p, name
        #szenen = mdb_get_table(db='set_Szenen')
        params = []
        inp_dict = {'name': u'Eingänge', 'type': 'group', 'expanded': True}
        inp_kinder = []
        for aktuator in self.inputs:   
            if aktuator.get('Name') <> None:
                title = aktuator.get('Description')
                akt_dict = {'name': aktuator.get('Name'), 'title':title , 'type': 'group', 'expanded': False}
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
        inp_dict = {'name': 'Speichern', 'type': 'group', 'children': [
                {'name': 'Speichere Inputs', 'type': 'action'}
            ]}   
        params.append(inp_dict)
        self.p = Parameter.create(name='params', type='group', children=params)
        self.p.param('Speichern', 'Speichere Inputs').sigActivated.connect(self.save)

    def save(self):
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)
        print neu_szene
        #mdb_set_table(table='set_Szenen', device=self.szene_to_read, commands=neu_szene)

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
                eingang = some_object.get('name')
                if eingang in self.eingaenge and eingang <> None:
                    for aktuator in self.inputs:
                        if aktuator.get('Name') == str(eingang):                    
                            for kind in some_object.get('children'):
                                wert = some_object.get('children').get(kind).get('value')
                                if wert == '': wert = None
                                if wert <> aktuator.get(kind):
                                    dicti[kind] = wert
                            mdb_set_table(table='cmd_inputs', device=aktuator.get('Name'), commands=dicti)
                else:
                    self.itera(some_object.get('children'))
            else:
                for item in some_object: 
                    self.itera(some_object.get(item))

#t = ParameterTree()
#sz=SzenenTreeInputs()
##print sz
#t.setParameters(sz.p, showTop=False)
#t.setWindowTitle('Szenen Setup:')
##t2 = ParameterTree()
##t2.setParameters(p, showTop=False)
#
#win = QtGui.QWidget()
#layout = QtGui.QGridLayout()
#win.setLayout(layout)
#layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)
#layout.addWidget(t, 20, 0, 1, 1)
##layout.addWidget(t2, 1, 1, 1, 1)
#win.show()
#win.resize(800,800)

            
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
                