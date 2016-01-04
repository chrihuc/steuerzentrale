#!/usr/bin/python
# -*- coding: utf-8 -*-

import constants

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV

from mysql_con import mdb_read_table_entry

from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *
import sys

descs = mdb_read_table_entry(constants.sql_tables.szenen.name,"Description")

xs1 = myezcontrol(constants.xs1_.IP)
hue = hue_lights()
sn = sonos()
tv = TV()
xs1_devs = xs1.list_devices()
hue_devs = hue.list_devices()
sns_devs = sn.list_devices()
tvs_devs = tv.list_devices()
System = None
Device = None


#tab Wecker
#tab settings
#   graphs for values
#tab timer
#tab szenen
#   modify
#   execute
#   add
#tab alarm events

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(700, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        
        # Keller
        self.tab_0 = QtGui.QWidget()
        #self.tab_0.setStyleSheet("QWidget {background-image:url(./EG.png)}")
        self.tab_0.setObjectName(_fromUtf8("Keller"))   
        self.tabWidget.addTab(self.tab_0, _fromUtf8(""))
        
        #Erdgeschoss
        self.tab = QtGui.QWidget()
        self.tab.setStyleSheet("QWidget {background-image:url(./EG.png)}")
        self.tab.setObjectName(_fromUtf8("Erdgeschoss"))
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 91, 24))
        self.pushButton.setObjectName(_fromUtf8("WohnziDecke"))
        self.pushButton.setText("Decke")
        self.pushButton.clicked.connect(lambda: self.set_popup("Wohnzimmer_Decke"))        
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        
        #1. Stock
        self.tab_1 = QtGui.QWidget()
        #self.tab_1.setStyleSheet("QWidget {background-image:url(./EG.png)}")
        self.tab_1.setObjectName(_fromUtf8("1_Stock"))   
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))  

        #2. Stock
        self.tab_2 = QtGui.QWidget()
        #self.tab_2.setStyleSheet("QWidget {background-image:url(./EG.png)}")
        self.tab_2.setObjectName(_fromUtf8("2_Stock"))   
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))          
        
        #Direkt
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.pushButton = QtGui.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(0, 10, 91, 24))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.xs1_clicked)
        self.pushButton_2 = QtGui.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 40, 91, 24))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.hue_clicked)
        self.pushButton_3 = QtGui.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 10, 91, 24))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_3.clicked.connect(self.sns_clicked)
        self.pushButton_4 = QtGui.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 40, 91, 24))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.tvs_clicked)        
        self.scrollLayout = QtGui.QFormLayout()
        self.scrollArea = QtGui.QScrollArea(self.tab_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 180, 380))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 165, 430))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def xs1_clicked(self):
        global System
        System = "XS1"
        self.clearLayout(self.scrollLayout)
        #while self.scrollLayout.rowCount() > 0:
            #self.scrollLayout.deleteLater()
        for item in xs1_devs:
            self.scrollLayout.addRow(Buttn(None,item,"Device"))

    def clearLayout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()

    def hue_clicked(self):
        global System
        System = "Hue"
        self.clearLayout(self.scrollLayout)
        for item in hue_devs:
            self.scrollLayout.addRow(Buttn(None,item,"Device"))

    def sns_clicked(self):
        global System
        System = "Sonos"
        self.clearLayout(self.scrollLayout)
        for item in sns_devs:
            self.scrollLayout.addRow(Buttn(None,item,"Device"))
            
    def tvs_clicked(self):
        global System
        System = "TV"
        self.clearLayout(self.scrollLayout)
        for item in tvs_devs:
            self.scrollLayout.addRow(Buttn(None,item,"Device"))            

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kontrollraum", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("MainWindow", "Keller", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Erdgeschoss", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "1. Stock", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "2. Stock", None))
        self.pushButton.setText(_translate("MainWindow", "XS1", None))
        self.pushButton_2.setText(_translate("MainWindow", "Hue", None))
        self.pushButton_3.setText(_translate("MainWindow", "Sonos", None))
        self.pushButton_4.setText(_translate("MainWindow", "TV", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Direkt", None))

    def set_popup(self,Name): 
        global Device
        Device = Name
        self.w = MyPopup(self,Name)
        self.w.setGeometry(QRect(500, 100, 200, 400))
        self.w.show() 

class Buttn(QtGui.QWidget):
    def __init__( self ,parent=None, Name=None, Type="Device"):
      super(Buttn, self).__init__(parent)

      if str(descs.get(Name)) <> "None":
        desc = str(descs.get(Name))
      else:
        desc= Name
      self.pushButton = QtGui.QPushButton(desc)
      
      layout = QtGui.QHBoxLayout()
      layout.addWidget(self.pushButton)
      if Type=="Device":
        self.pushButton.clicked.connect(lambda: self.set_popup(Name)) 
      elif Type=="Command":
        self.pushButton.clicked.connect(lambda: self.send_command(Name))         
      self.setLayout(layout)
      
    def set_popup(self,Name): 
        global Device
        Device = Name
        self.w = MyPopup(self,Name)
        self.w.setGeometry(QRect(500, 100, 200, 400))
        self.w.show() 
        
    def send_command(self,Command):
        print Device, Command
        if System == "Sonos":
            sn.set_device(player=Device, command=Command)
        elif System == "XS1":
            xs1.set_device(Device, Command)   
        elif System == "Hue":
            hue.set_device(Device, Command)   
        elif System == "TV":
            hue.set_device(Device, Command)             

class MyPopup(QtGui.QMainWindow):
    def __init__(self, parent=None, Text="Test"):
        #super(MyPopup, self).__init__(parent)
        global System
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle(Text)
        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.scrollArea) 
        
        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)          

        if Text in xs1_devs:
            System = "XS1"
            for item in xs1.list_commands():
                self.scrollLayout.addRow(Buttn(self,str(item),"Command"))
        elif Text in hue_devs:
            System = "Hue"
            for item in hue.list_commands():
                self.scrollLayout.addRow(Buttn(self,str(item),"Command"))       
        elif Text in sns_devs:
            System = "Sonos"
            for item in sn.list_commands():
                self.scrollLayout.addRow(Buttn(self,str(item),"Command"))     
        elif Text in tvs_devs:
            System = "TV"
            for item in tv.list_commands():
                self.scrollLayout.addRow(Buttn(self,str(item),"Command"))                  
        
    #def paintEvent(self, e):
        #self.scrollLayout.addRow(Test("test"))
        #pass
        #dc = QtGui.QPainter(self)
        #dc.drawLine(0, 0, 100, 100)
        #dc.drawLine(100, 0, 0, 100)

app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.setGeometry(QRect(0, 0, 800, 500))
myWidget.show()
app.exec_() 
