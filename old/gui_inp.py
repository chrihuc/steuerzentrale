# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 13:15:11 2016

@author: christoph
"""

import constants

from pyqtgraph.Qt import QtCore, QtGui
from mysql_con import mdb_get_table, mdb_set_table

app = QtGui.QApplication([])
from pyqtgraph.parametertree import Parameter, ParameterTree

from cmd_szenen import szenen
from cmd_satellites import satelliten

szn = szenen()
szn_lst = sorted(szn.list_commands('alle'))

cmdLsts = ['out_hue','out_Sonos']
sate = satelliten()
cmdLsts += sate.listCommandTable('alle')

sets = mdb_get_table(constants.sql_tables.settings.name)


class SzenenTreeInputs():
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
        global p, name
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
        params.append(dicti)
        self.p = Parameter.create(name='params', type='group', children=params)

    def save(self):
        global state
        self.state = self.p.saveState()
        neu_szene = self.itera(self.state)

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
                        if str(aktuator.get('Id')) == str(eingang):  
                            for kind in some_object.get('children'):
                                wert = some_object.get('children').get(kind).get('value')
                                if wert == '': wert = None
                                if wert <> aktuator.get(kind):
                                    dicti[kind] = wert
                            if self.isInputs:
                                mdb_set_table(table='cmd_inputs', device=str(aktuator.get('Id')), commands=dicti, primary = 'Id')
                else:
                    self.itera(some_object.get('children'))
            else:
                for item in some_object: 
                    self.itera(some_object.get(item))

def selected(text):
    global sz, t
    sz=SzenenTreeInputs(False,text)
    t.setParameters(sz.p, showTop=False)


win = QtGui.QWidget()
comboBox = QtGui.QComboBox(win)
for cmdLst in cmdLsts:
    comboBox.addItem(cmdLst)
comboBox.activated[str].connect(selected)
t = ParameterTree()
sz=SzenenTreeInputs(False,cmdLsts[0])
#print sz
t.setParameters(sz.p, showTop=False)
t.setWindowTitle('Szenen Setup:')
#t2 = ParameterTree()
#t2.setParameters(p, showTop=False)


    
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel(""), 1,  1, 1, 2)

layout.addWidget(comboBox, 0, 0, 1, 1)
layout.addWidget(t, 20, 0, 1, 1)
#layout.addWidget(t2, 1, 1, 1, 1)
win.show()
win.resize(800,800)

            
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
                