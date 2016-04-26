# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 09:12:30 2016

@author: christoph
"""

from pyqtgraph.flowchart import Flowchart
fc = Flowchart(terminals={
    'nameOfInputTerminal': {'io': 'in'},
    'nameOfOutputTerminal': {'io': 'out'}
})

ctrl = fc.ctrlWidget()
myLayout.addWidget(ctrl)  ## read Qt docs on QWidget and layouts for more information