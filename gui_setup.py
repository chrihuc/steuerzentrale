# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:53:28 2016

@author: christoph
"""

from gui_szenen import Szenen_tree
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.Qt import QtCore, QtGui

t = ParameterTree()
sz=Szenen_tree("TV")
t.setParameters(sz.p, showTop=False)
t.setWindowTitle('Szenen Setup:')
#t2 = ParameterTree()
#t2.setParameters(p, showTop=False)

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)
layout.addWidget(t, 1, 0, 1, 1)
#layout.addWidget(t2, 1, 1, 1, 1)
win.show()
win.resize(800,800)