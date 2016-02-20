# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 06:56:07 2016

@author: chuckle
"""

#import pyqtgraph.examples
#pyqtgraph.examples.run()

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

win = pg.GraphicsWindow(title="Basic plotting examples")
#win.resize(1000,600)
win.setWindowTitle('Homecontrol Graph')

graph = np.array([0,1,2,3,4,3,2,1])#np.random.normal(size=100)

p1 = win.addPlot(title="Whatever", y=graph)
