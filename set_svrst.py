# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 07:44:56 2016

@author: christoph
"""

import constants

from os.path import expanduser
from PyQt4 import QtGui, QtCore
import sqlsync
from cmd_satellites import satelliten

#startingDir = cmds.workspace(q=True, rootDirectory=True)
#destDir = QtGui.QFileDialog.getExistingDirectory(None, 
#                                                 'Open working directory', 
#                                                 startingDir, 
#                                                 QtGui.QFileDialog.ShowDirsOnly)
        
app = QtGui.QApplication([])
sat = satelliten()
#win = QtGui.QWidget()   
#get folder                                      
my_dir = QtGui.QFileDialog.getExistingDirectory(
    None,
    "Open a folder",
    expanduser("~"),
    QtGui.QFileDialog.ShowDirsOnly
)

ssync = sqlsync.sync()

syncliste = []
syncliste += ["cmd_inputs"]
syncliste += ["out_hue"]
syncliste += ["out_Sonos"]
syncliste += ["set_satellites"]
syncliste += sat.listCommandTable(device="forSave", nameReturn = False)
syncliste += ["set_settings"]
syncliste += ["set_Szenen"]

print my_dir
print syncliste

#Save
for table in syncliste:
    try:
        ssync.export(table, db=constants.sql_.DB, for_git = False, folder=my_dir)
    except:
        print "Fehler"
app.quit()
#app.exec_() 