#!/usr/bin/python
# -*- coding: utf-8 -*-

import constants

from outputs import sonos
from outputs import xs1
from outputs import hue
from outputs import samsung
from outputs import satellites
from outputs import szenen
from outputs import cron
from alarm_event_messaging import alarmevents
#from gui_szenen import Szenen_tree

from database import mysql_connector as msqc

from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *
import sys
import git
import pyqtgraph as pg
import numpy as np
from threading import Timer
import subprocess as sp
import threading
import time
import datetime
import os
import socket
#import win32api
import random

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree

import urllib2

descs = msqc.mdb_read_table_entry(constants.sql_tables.szenen.name,"Description")

aes = alarmevents.AES()

xs1 = xs1.XS1(constants.xs1_.IP)
hue = hue.Hue_lights()
sn = sonos.Sonos()
tv = samsung.TV()
sat = satellites.Satellite()
szn = szenen.Szenen()
crons = cron.Cron()
xs1_devs = xs1.list_devices()
hue_devs = hue.list_devices()
sns_devs = sn.list_devices()
tvs_devs = tv.list_devices()
sat_devs = sat.list_devices()
szn_cmds = szn.list_commands()
szn_favs = szn.list_commands(gruppe='Favorit')
System = None
Device = None
constants.redundancy_.master = True

eg_buttons = [{'Name':'A00TER1GEN1TE01','desc':'T Balkon','type':'sens','pos_x':5,'pos_y':150},
              {'Name':'V00WOH1RUM1CO01','desc':'CO2','type':'sens','pos_x':150,'pos_y':150},
              {'Name':'V00WOH1RUM1TE01','desc':'T Balkon','type':'sens','pos_x':150,'pos_y':20},
              {'Name':'V00KUE1RUM1TE02','desc':'T Kueche','type':'sens','pos_x':650,'pos_y':175},
              {'Name':'V00KUE1DEK1LI01','desc':'Decke','type':'dev','pos_x':700,'pos_y':270},
              {'Name':'V00KUE1DEK1LI02','desc':'Decke','type':'dev','pos_x':500,'pos_y':290},
              {'Name':'V00WOH1DEK1LI01','desc':'Decke','type':'dev','pos_x':390,'pos_y':270}]
              
og_buttons = [{'Name':'V01BUE1RUM1LI01','desc':u'Büro','type':'dev','pos_x':150,'pos_y':300},
              {'Name':'V01BAD1RUM1TE01','desc':'T Balkon','type':'sens','pos_x':550,'pos_y':120},
              {'Name':'V01BAD1RUM1HU01','desc':'T Balkon','type':'sens','pos_x':600,'pos_y':120},
              {'Name':'V01SCH1RUM1TE01','desc':'T Balkon','type':'sens','pos_x':450,'pos_y':300},
              {'Name':'V01KID1RUM1TE01','desc':'T Kind','type':'sens','pos_x':150,'pos_y':20}
              ]
              
dg_buttons = [{'Name':'V02ZIM1RUM1TE02','desc':u'Büro','type':'sens','pos_x':500,'pos_y':260}]              

weckerButtons = []
SchaltUhren = []

#tab Wecker
#tab settings
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

running = True
streaming = True
        
class LoadImageThread(QtCore.QThread):
        def __init__(self):
            QtCore.QThread.__init__(self)
     
        def __del__(self):
            self.wait()
            
        def run(self):
            if streaming:
                self.emit(QtCore.SIGNAL('showImage()'))
                refresh = Timer(.5, self.run, [])
                refresh.start()

class RefreshGuiThread(QtCore.QThread):
        def __init__(self):
            QtCore.QThread.__init__(self)
     
        def __del__(self):
            self.wait()
            
        def run(self):
            if running:
                self.emit(QtCore.SIGNAL('update_values()'))
                refresh = Timer(15, self.run, [])
                refresh.start()

class ListenUdpThread(QtCore.QThread):
        def __init__(self):
            QtCore.QThread.__init__(self)
            self.active = True
            self.broadSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            hostName = socket.gethostbyname( '192.168.192.255')#constants.eigene_IP )
            self.broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.broadSocket.bind( (hostName, constants.udp_.broadPORT)) 
            self.set_screensaver()
            threading.Thread(target=self.screensaver).start()
            
     
        def __del__(self):
            self.wait()
        
        def set_screensaver(self):
            if constants.gui_.KS:
                exectext = "xset -dpms"
                os.system(exectext)    
                exectext = "xset s off"
                os.system(exectext)   
#                exectext = "xset s ''"
#                os.system(exectext)                 
            
        def screensaver(self, threshold=15000):
            import thread
            # note that sys.stdout.write and .flush should rather be used
            # instead of print
            while constants.gui_.KS and running:
                try:
                    idle = float(sp.check_output('xprintidle', shell=True).strip())
                    if idle > threshold and self.active:
                        self.emit(QtCore.SIGNAL('show_homepage()'))
                        if msqc.settings_r()['Status'] == 'Wach' and constants.gui_.Feh:
                            print "Start feh"
#                            exectext = 'xbindkeys -n -f xbindkeys.temp'
#                            os.system(exectext) 
                            exectext = "feh -F -D 20 --randomize /home/pi/Pictures/* &"
                            os.system(exectext)                            
                        else:
                            exectext = "pkill feh"
                            os.system(exectext)                            
                            exectext = "DISPLAY=:0 xset dpms force off"
                            os.system(exectext)
                        self.active = False
                    if idle < threshold and not self.active:
                        exectext = "DISPLAY=:0 xset dpms force on"
                        os.system(exectext)
                        exectext = "pkill feh"
                        os.system(exectext)
                        print "Kill feh"
                        self.active = True
                        self.set_screensaver()
                except (ValueError, sp.CalledProcessError) as err:
                    print 'An error occured'
                    # add your error handling here
                time.sleep(0.2)
#            thread.interrupt_main()                
        def disp_an(self):
            idle = float(sp.check_output('xprintidle', shell=True).strip())
            exectext = "DISPLAY=:0 xset dpms force on"
            os.system(exectext) 
            exectext = "feh -F -D 20 --randomize /home/pi/Pictures/* &"
            os.system(exectext) 
            self.set_screensaver()

        def disp_aus(self):
            exectext = "pkill feh"
            os.system(exectext)                            
            exectext = "DISPLAY=:0 xset dpms force off"
            os.system(exectext)

        def run(self):
            SIZE = 1024
            while running:
                try:
                    (data,addr) = self.broadSocket.recvfrom(SIZE)
                    print data
                    if not data:
                        break
                    isdict = False
                    try:
                        data_ev = eval(data)
                        if type(data_ev) is dict:
                            isdict = True
                    except Exception as serr:
                        isdict = False  
                    if isdict:
                        if data_ev['Name'] == 'Klingel':
                            self.emit(QtCore.SIGNAL('showCam()'))  
                        elif data_ev['Name'] == 'DisplayAn':
                            self.disp_an()
                        elif data_ev['Name'] == 'DisplayAus':
                            self.disp_aus()                         
                except socket.error, e:
                    if e.errno != 4:
                        raise                
        
class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.set_buttons = [{'Name':'xs1_clicked','desc':'XS1','type':'int','command':self.xs1_clicked,'pos_x':0,'pos_y':10}]
        self.setupUi(self)
#        self.set_screensaver()
    
    def show_homepage(self):
        self.tabWidget.setCurrentIndex(constants.gui_.Home)
    
    def set_fullscreen(self):
        super(Main, self).showFullScreen()
        
    def set_normalscreen(self):
        super(Main, self).showNormal()        
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(700, 500)
        settings = msqc.settings_r()
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 50px;}")
        
        # Time
        self.ti_lbl = QtGui.QLabel(self.tabWidget)
        self.ti_lbl.setText(str(datetime.datetime.now().strftime('%d. %m. %H:%M')))
        self.ti_lbl.setGeometry(QtCore.QRect(720, 15, 100, 20)) 
        self.ti_lbl.setStyleSheet("QLabel { background-color : white; color : black; }")
        
        # Keller
        self.tab_0 = QtGui.QWidget()
        self.tab_0.setStyleSheet("QWidget {background-image:url(./media/UG.png)}")
        self.tab_0.setObjectName(_fromUtf8("Keller"))   
        self.tabWidget.addTab(self.tab_0, _fromUtf8(""))
        
        #Erdgeschoss
        self.tab = QtGui.QWidget()
        
        self.tab.setObjectName(_fromUtf8("Erdgeschoss")) 
        self.tab.setStyleSheet("background-image:url(./media/EG.png)")
        self.buttons = []
        for btn in eg_buttons:
            self.buttons.append(QtGui.QPushButton(self.tab))
            self.buttons[-1].setGeometry(QtCore.QRect(btn.get('pos_x'), btn.get('pos_y'), 50, 50))
            self.buttons[-1].setObjectName(btn.get('Name'))
            self.buttons[-1].setStyleSheet("background-image:url(./media/EG3.png);background-color: rgb(255,255,255);border: 2px solid #222222")
            if btn.get('type') == 'dev':
                self.buttons[-1].clicked.connect(self.make_set_popup(btn.get('Name')))
                self.buttons[-1].setText(_fromUtf8(btn.get('desc')))
            elif btn.get('type') == 'sens':
                self.buttons[-1].clicked.connect(self.make_set_g_popup(btn.get('Name')))
                self.buttons[-1].setText(settings.get(btn.get('Name'))) 
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        
        #1. Stock
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setStyleSheet("QWidget {background-image:url(./media/OG.png)}")
        self.tab_1.setObjectName(_fromUtf8("1_Stock"))   
        for btn in og_buttons:
            self.buttons.append(QtGui.QPushButton(self.tab_1))
            self.buttons[-1].setGeometry(QtCore.QRect(btn.get('pos_x'), btn.get('pos_y'), 50, 50))
            self.buttons[-1].setObjectName(btn.get('Name'))
            if btn.get('type') == 'dev':
                self.buttons[-1].clicked.connect(self.make_set_popup(btn.get('Name')))
                self.buttons[-1].setText(_fromUtf8(btn.get('desc')))
            elif btn.get('type') == 'sens':
                self.buttons[-1].clicked.connect(self.make_set_g_popup(btn.get('Name')))
                self.buttons[-1].setText(settings.get(btn.get('Name')))          
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))  

        #2. Stock
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setStyleSheet("QWidget {background-image:url(./media/DG.png)}")
        self.tab_2.setObjectName(_fromUtf8("2_Stock")) 
        for btn in dg_buttons:
            self.buttons.append(QtGui.QPushButton(self.tab_2))
            self.buttons[-1].setGeometry(QtCore.QRect(btn.get('pos_x'), btn.get('pos_y'), 50, 50))
            self.buttons[-1].setObjectName(btn.get('Name'))
            if btn.get('type') == 'dev':
                self.buttons[-1].clicked.connect(self.make_set_popup(btn.get('Name')))
                self.buttons[-1].setText(_fromUtf8(btn.get('desc')))
            elif btn.get('type') == 'sens':
                self.buttons[-1].clicked.connect(self.make_set_g_popup(btn.get('Name')))
                self.buttons[-1].setText(settings.get(btn.get('Name')))         
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))          
        
        #Direkt
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        for btn in self.set_buttons:
            self.buttons.append(QtGui.QPushButton(self.tab_3))
            self.buttons[-1].setGeometry(QtCore.QRect(btn.get('pos_x'), btn.get('pos_y'), 91, 24))
            self.buttons[-1].setObjectName(btn.get('Name'))
            if btn.get('type') == 'dev':
                self.buttons[-1].clicked.connect(self.make_set_popup(btn.get('Name')))
                self.buttons[-1].setText(_fromUtf8(btn.get('desc')))
            elif btn.get('type') == 'sens':
                self.buttons[-1].clicked.connect(self.make_set_g_popup(btn.get('Name')))
                self.buttons[-1].setText(settings.get(btn.get('Name'))) 
            elif btn.get('type') == 'int':
                self.buttons[-1].clicked.connect(btn.get('command'))
                self.buttons[-1].setText(_fromUtf8(btn.get('desc')))                 
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
        self.pushButton_5 = QtGui.QPushButton(self.tab_3)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 10, 91, 24))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.sat_clicked)          
        self.scrollLayout = QtGui.QFormLayout()
        self.scrollArea = QtGui.QScrollArea(self.tab_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 250, 350))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 0, 360))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollLayout2 = QtGui.QFormLayout()
        self.scrollArea2 = QtGui.QScrollArea(self.tab_3)
        self.scrollArea2.setGeometry(QtCore.QRect(260, 70, 250, 350))
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setObjectName(_fromUtf8("scrollArea2"))
        self.scrollAreaWidgetContents2 = QtGui.QWidget()
        self.scrollAreaWidgetContents2.setGeometry(QtCore.QRect(0, 0, 165, 360))
        self.scrollAreaWidgetContents2.setObjectName(_fromUtf8("scrollAreaWidgetContents2"))
        self.scrollAreaWidgetContents2.setLayout(self.scrollLayout2)        
        self.scrollArea2.setWidget(self.scrollAreaWidgetContents2)   
#        self.scrollArea2.scrollBar.setStyleSheet("""QScrollBar:vertical {
#        width:30px;
#        }""")
        self.xs1_clicked()
        self.fill_szenen_favs()
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        
        #Settings
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.pushButton_6 = QtGui.QPushButton(self.tab_4)
        self.pushButton_6.setGeometry(QtCore.QRect(0, 10, 100, 50))
        self.pushButton_6.setObjectName(_fromUtf8("gitupdate"))
        self.pushButton_6.clicked.connect(self.git_update)    
        self.pushButton_7 = QtGui.QPushButton(self.tab_4)
        self.pushButton_7.setGeometry(QtCore.QRect(0, 110, 100, 50))
        self.pushButton_7.setObjectName(_fromUtf8("gitupdate"))
        self.pushButton_7.setText('Update')
        self.pushButton_7.clicked.connect(self.update_values)     
        self.pushButton_8 = QtGui.QPushButton(self.tab_4)
        self.pushButton_8.setGeometry(QtCore.QRect(140, 10, 100, 50))
        self.pushButton_8.setObjectName(_fromUtf8("AEs"))
        self.pushButton_8.setText('AlarmEvents')
        self.pushButton_8.clicked.connect(self.showAlarmEvents)   
        self.pushButton_9 = QtGui.QPushButton(self.tab_4)
        self.pushButton_9.setGeometry(QtCore.QRect(140, 110, 100, 50))
        self.pushButton_9.setObjectName(_fromUtf8("Close"))
        self.pushButton_9.setText('Close')
        self.pushButton_9.clicked.connect(self.close)    
        self.pushButton_19 = QtGui.QPushButton(self.tab_4)
        self.pushButton_19.setGeometry(QtCore.QRect(280, 10, 100, 50))
        self.pushButton_19.setObjectName(_fromUtf8("Fullscreen"))
        self.pushButton_19.setText('Fullscreen')
        self.pushButton_19.clicked.connect(self.set_fullscreen) 
        self.pushButton_29 = QtGui.QPushButton(self.tab_4)
        self.pushButton_29.setGeometry(QtCore.QRect(280, 110, 100, 50))
        self.pushButton_29.setObjectName(_fromUtf8("Normal"))
        self.pushButton_29.setText('Normal')
        self.pushButton_29.clicked.connect(self.set_normalscreen)         
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))

        #Wecker
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5")) 
        self.tabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.scrollLayout3 = QtGui.QFormLayout()
        self.scrollArea = QtGui.QScrollArea(self.tab_5)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 790, 350))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 165, 340))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout3)        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)  
        self.lbl = QtGui.QLabel(self.tab_5)
        self.lbl.setText(self.checkWecker())
        self.lbl.setGeometry(QtCore.QRect(120, 360, 500, 50))
        
        #self.add_wecker()
        self.pushButton_9 = QtGui.QPushButton(self.tab_5)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 360, 91, 50))
        self.pushButton_9.setObjectName(_fromUtf8("saveAlarm"))
        self.pushButton_9.setText('Speichere')
        self.pushButton_9.clicked.connect(self.makeSaveWecker(self)) 
        
        #Schaltuhr
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName(_fromUtf8("tab_5")) 
        self.tabWidget.addTab(self.tab_7, _fromUtf8(""))
        self.scrollLayout4 = QtGui.QFormLayout()
        self.scrollArea = QtGui.QScrollArea(self.tab_7)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 790, 350))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 165, 340))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout4)        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)  
        
        #self.add_wecker()
        self.pushButton_12 = QtGui.QPushButton(self.tab_7)
        self.pushButton_12.setGeometry(QtCore.QRect(10, 360, 91, 50))
        self.pushButton_12.setObjectName(_fromUtf8("saveAlarm"))
        self.pushButton_12.setText('Speichere')
        self.pushButton_12.clicked.connect(self.makeSaveSchaltUhr(self)) 
        
        self.tab_7.connect(self.tabWidget, SIGNAL('currentChanged(int)'), self.update)
        
        #Cam
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6")) 
        self.layout_Cam = QtGui.QFormLayout(self.tab_6)
        self.tabWidget.addTab(self.tab_6, _fromUtf8(""))  
        self.tab_6.connect(self.tabWidget, SIGNAL('currentChanged(int)'), self.update)
        self.lbl2 = QtGui.QLabel(self.tab_6)
        self.lbl2.setGeometry(100, 100, 400, 100)
        self.pushButton_10 = QtGui.QPushButton(self.tab_6)
        self.pushButton_10.setGeometry(QtCore.QRect(550, 50, 100, 100))
#        self.pushButton_10.setObjectName(_fromUtf8("saveAlarm"))
        self.pushButton_10.setText('Update')
        self.pushButton_10.clicked.connect(lambda: self.updateImage()) 

        self.pushButton_111 = QtGui.QPushButton(self.tab_6)
        self.pushButton_111.setGeometry(QtCore.QRect(550, 150, 100, 100))
#        self.pushButton_111.setObjectName(_fromUtf8("SaveAlarm"))
        self.pushButton_111.setText('Play')
#        self.pushButton_111.setCheckable(True)
        self.pushButton_111.clicked.connect(self.makeload_cam(self)) 

        self.pushButton_11 = QtGui.QPushButton(self.tab_6)
        self.pushButton_11.setGeometry(QtCore.QRect(550, 250, 100, 100))
#        self.pushButton_11.setObjectName(_fromUtf8("saveAlarm"))
        self.pushButton_11.setText('Stop')
        self.pushButton_11.clicked.connect(self.makestop(self)) 
        self.layout_Cam.setGeometry(QtCore.QRect(150, 250, 100, 100))
        self.load_cam()
#        lbl = QtGui.QLabel(self)
#        lbl.setPixmap(QtGui.QPixmap(image))
      
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(constants.gui_.Home)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        thread_ref = RefreshGuiThread()
        self.connect(thread_ref, QtCore.SIGNAL("update_values()"), self.update_values)
        thread_ref.start()  
        udpt = ListenUdpThread()
        udptt = Timer(0, udpt.run, [])
        self.connect(udpt, QtCore.SIGNAL("showCam()"), self.showCam)
        self.connect(udpt, QtCore.SIGNAL("show_homepage()"), self.show_homepage)
        udptt.start()     

    def add_wecker(self):
        global weckerButtons
        self.clearLayout(self.scrollLayout3)
        weckerButtons = []
        wecker = crons.get_all(wecker=True)
        for i in wecker:
            self.scrollLayout3.addRow(weckerRow(i))

    def add_SchaltUhr(self):
        global SchaltUhren
        self.clearLayout(self.scrollLayout4)
        SchaltUhren = []
        wecker = crons.get_all(typ='Gui')
        for i in wecker:
            self.scrollLayout4.addRow(weckerRow(i, wecker=False) )           
            
    def makeload_cam(self,parent=None):  
        print('load cam')
        def wrapper():
            global streaming
            streaming = True 
            self.refresh()
        return wrapper

    def makeload_cam1x(self,parent=None):
        print('load cam 1')
        def wrapper(): 
            self.load_cam()
        return wrapper

    def makestop(self,parent=None):
        def stoper():
            global streaming
            streaming = False
        return stoper        
        
    def refresh(self):
        thread = LoadImageThread()
        self.connect(thread, QtCore.SIGNAL("showImage()"), self.updateImage)
        thread.start()         

    def showCam(self):
        if constants.gui_.KlingelAn:
            exectext = "DISPLAY=:0 xset dpms force on"
            os.system(exectext)             
        self.tabWidget.setCurrentIndex(8)
        self.updateImage()
        scres = Timer(30, self.show_homepage, [])
        scres.start()

    def load_cam(self):
        QtGui.QApplication.processEvents()
        self.clearLayout(self.layout_Cam)
        self.hbox = QtGui.QHBoxLayout()
        url = 'http://192.168.192.36/html/cam.jpg'

        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
            data = response.read()  
        except urllib2.URLError as e:
            data = None

        image = QtGui.QImage()
        image.loadFromData(data)
        
#        self.lbl2 = QtGui.QLabel(self.tab_6)
#        self.lbl2.setMinimumSize(1, 1)
#        self.lbl2.setScaledContents(True)
        self.lbl2.setPixmap(QtGui.QPixmap(image))
        self.hbox.addWidget(self.lbl2)
        self.layout_Cam.addRow(QtGui.QLabel(""),self.hbox)
        self.lbl2.setGeometry(100, 100, 400, 100)
        self.lbl2.move(100,100)
        self.hbox.setGeometry(QtCore.QRect(100, 100, 400, 100))
        self.tab_6.setLayout(self.layout_Cam)
      
    @QtCore.pyqtSlot(str)
    def updateImage(self):
        print('updating')
        url = 'http://192.168.192.36/html/cam.jpg'
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
            data = response.read()  
        except urllib2.URLError as e:
            data = None
        image = QtGui.QImage()
        image.loadFromData(data)        
        pixmap = QtGui.QPixmap(image)
        self.lbl2.setPixmap(pixmap)        
            
    def update(self):
        if self.tabWidget.currentIndex() ==6:
            self.add_wecker()
            self.update_values()
        if self.tabWidget.currentIndex() ==7:
            self.add_SchaltUhr()            
#        if self.tabWidget.currentIndex() ==8:
#            self.load_cam()

    def update_values(self):
        settings = msqc.settings_r()
        for btn in self.buttons:
            name = btn.objectName()
            if str(name) in settings:
#                print name, settings.get(str(name))
                btn.setText(settings.get(str(name)))
        self.ti_lbl.setText(str(datetime.datetime.now().strftime('%d. %m. %H:%M')))
        QtGui.QApplication.processEvents()             

    def close_clicked(self):
        QtCore.QCoreApplication.instance().quit()

    def git_update(self):
        global running
        g = git.cmd.Git()
        g.reset('--hard')
        g.pull()
        running = False
        sys.exit()
        QtCore.QCoreApplication.instance().quit()

    def close(self):
        global running
        running = False
        print running
#        import thread
#        thread.interrupt_main() 
        QtCore.QCoreApplication.instance().quit()
        sys.exit()        

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

    def sat_clicked(self):
        global System
        System = "Satelliten"
        self.clearLayout(self.scrollLayout)
        for item in sat_devs:
            self.scrollLayout.setContentsMargins(0, 5, 5, 5)
            self.scrollLayout.addRow(Buttn(None,item,"Device")) 

    def fill_szenen_favs(self):
        self.clearLayout(self.scrollLayout2)
        #while self.scrollLayout.rowCount() > 0:
            #self.scrollLayout.deleteLater()
        for item in szn_favs:
            if szn_favs.get(item) <> "":
                self.scrollLayout2.addRow(Buttn(None,Name=item,Type="Szene",description=szn_favs.get(item) ))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kontrollraum", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("MainWindow", "Keller", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Erdgeschoss", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "1. Stock", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "2. Stock", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Wecker", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "Schaltuhr", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Kamera", None))
        #self.pushButton.setText(_translate("MainWindow", "XS1", None))
        self.pushButton_2.setText(_translate("MainWindow", "Hue", None))
        self.pushButton_3.setText(_translate("MainWindow", "Sonos", None))
        self.pushButton_4.setText(_translate("MainWindow", "TV", None))
        self.pushButton_5.setText(_translate("MainWindow", "Satelliten", None))
        self.pushButton_6.setText(_translate("MainWindow", "GIT Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Direkt", None))

    def set_popup(self,Name): 
        global Device
        Device = Name
        self.w = MyPopup(self,Name)
        self.w.setGeometry(QRect(500, 100, 200, 400))
        self.w.show() 
        return True
        
    def make_set_popup(self, Name):
        def set_popup(): 
            global Device
            Device = Name
            self.w = MyPopup(self,Name)
            self.w.setGeometry(QRect(500, 100, 200, 400))
            self.w.show() 
        return set_popup
        
    def make_set_g_popup(self, Name):
        def set_g_popup(): 
            self.w = MyGraphPopup(self,Name)
            #self.w.setGeometry(QRect(500, 100, 200, 400))
            self.w.show() 
        return set_g_popup

    def make_set_tree_popup(self, Name):
        def set_tree_popup(): 
            self.w = MySZTreePopup(self,Name)
            #self.w.setGeometry(QRect(500, 100, 200, 400))
            self.w.show() 
        return set_tree_popup      


    def makeSaveWecker(self,parent=None):
        def saveWecker(self):
            parent = {}
            for ii in weckerButtons:
                name = ii.objectName().split('.')[0]
                if name in parent:
                    child = parent.get(name)
                else:
                    parent[name] = {}
                    child = {'Name':name}
                if "timeEdit" in ii.objectName():
                    child['Time'] = ii.time().toString('HH:mm')
                elif "comboBox" in ii.objectName():
                    child['Szene'] = ii.currentText()
                else:   
                    if ii.checkState()  == 2:
                        child[ii.objectName().split('.')[1]] = True
                    else:
                        child[ii.objectName().split('.')[1]] = False
                parent[name] = child
            liste = []
            for wecker in parent:
                liste.append(parent.get(wecker))
                msqc.mdb_set_table(table=constants.sql_tables.cron.name, device=parent.get(wecker).get('Name'), commands=parent.get(wecker), primary = 'Name')
        time.sleep(1)
        self.lbl.setText(self.checkWecker())
        QApplication.processEvents()
        return saveWecker 
      
    def makeSaveSchaltUhr(self,parent=None):
        def saveSchaltUhr(self):
            parent = {}
            for ii in SchaltUhren:
                name = ii.objectName().split('.')[0]
                if name in parent:
                    child = parent.get(name)
                else:
                    parent[name] = {}
                    child = {'Name':name}
                if "timeEdit" in ii.objectName():
                    child['Time'] = ii.time().toString('HH:mm')
                elif "comboBox" in ii.objectName():
                    child['Szene'] = ii.currentText()
                else:   
                    if ii.checkState()  == 2:
                        child[ii.objectName().split('.')[1]] = True
                    else:
                        child[ii.objectName().split('.')[1]] = False
                parent[name] = child
            liste = []
            for wecker in parent:
                liste.append(parent.get(wecker))
                msqc.mdb_set_table(table=constants.sql_tables.cron.name, device=parent.get(wecker).get('Name'), commands=parent.get(wecker), primary = 'Name')
        QApplication.processEvents()
        return saveSchaltUhr     
    
    def checkWecker(self):
        next_i = crons.next_wecker_heute_morgen()
        return next_i

    def showAlarmEvents(self): 
        self.w = AEPopup(self)
        self.w.setGeometry(QRect(500, 100, 200, 400))
        self.w.show() 
        return True        
        
class weckerRow(QtGui.QWidget):
    def __init__( self ,weckerList, wecker=True):
        global weckerButtons, SchaltUhren
        super(weckerRow, self).__init__(None)
        print weckerList
        #horizontalLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        #horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 391, 61))
        #horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        horizontalLayoutWidget = QtGui.QHBoxLayout()
        #horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.font = QtGui.QFont()
        if not constants.gui_.KS:
            self.font.setPixelSize(15)
        self.timeEdit = QtGui.QTimeEdit()
        name = weckerList.get('Name')
        self.timeEdit.setObjectName(_fromUtf8(str(name)+".timeEdit"))
        self.timeEdit.setTime((datetime.datetime.min+weckerList.get('Time')).time())
        self.timeEdit.setDisplayFormat("HH:mm")
        self.timeEdit.setMinimumSize(130,50)
        self.timeEdit.setStyleSheet("""
        QTimeEdit::up-button { subcontrol-position: left; width: 40px; height: 40px;}
        QTimeEdit::down-button { subcontrol-position: right; width: 40px; height: 40px;} """)
        self.timeEdit.setFont(self.font)
        horizontalLayoutWidget.addWidget(self.timeEdit)
        if wecker:
            weckerButtons.append(self.timeEdit)
        else:
            SchaltUhren.append(self.timeEdit)
        for tag in ['Mo','Di','Mi','Do','Fr','Sa','So','Eingeschaltet']:
            self.checkBox = QtGui.QCheckBox(tag)
            self.checkBox.setObjectName(_fromUtf8(str(name)+"."+tag))
            horizontalLayoutWidget.addWidget(self.checkBox)
            if wecker:
                weckerButtons.append(self.checkBox)
            else:
                SchaltUhren.append(self.checkBox)                
            self.checkBox.setChecked(eval(weckerList.get(tag)))
        self.comboBox = QtGui.QComboBox()
        if wecker:
            SzenenList = szn.list_commands("Wecker")
        else:
            SzenenList = szn.list_commands()
        for szne in SzenenList:
            self.comboBox.addItem(szne)    
        index = self.comboBox.findText(weckerList.get('Szene'), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox.setCurrentIndex(index)
        self.comboBox.setObjectName(_fromUtf8(str(name)+".comboBox"))
        if wecker:        
            weckerButtons.append(self.comboBox)
        else:
            SchaltUhren.append(self.comboBox)            
        horizontalLayoutWidget.addWidget(self.comboBox)
        #self.scrollArea.setWidget(self.scrollAreaWidgetContents) 
        self.setLayout(horizontalLayoutWidget)

class Buttn(QtGui.QWidget):
    def __init__( self ,parent=None, Name=None, Type="Device", description=None):
      super(Buttn, self).__init__(parent)
      self.parent = parent
      if str(descs.get(Name)) <> "None":
        desc = str(descs.get(Name))
      elif description <> None:
        desc = description
      else:
        desc= Name
      self.pushButton = QtGui.QPushButton(desc)
      self.pushButton.setGeometry(QtCore.QRect(0, 0, 300, 300))
      self.pushButton.setMinimumHeight(50)
      layout = QtGui.QHBoxLayout()
      layout.setGeometry(QtCore.QRect(0, 0, 300, 300))
      layout.addWidget(self.pushButton)
      if Type=="Device":
        self.pushButton.clicked.connect(lambda: self.set_popup(Name)) 
      elif Type=="Command":
        self.pushButton.clicked.connect(lambda: self.send_command(Name))       
      elif Type=="Szene":
        self.pushButton.clicked.connect(lambda: self.execute_on_server(Name))          
      self.setLayout(layout)
      
    def set_popup(self,Name): 
        global Device
        Device = Name
        self.w = MyPopup(self,Name)
        self.w.setGeometry(QRect(500, 100, 200, 400))
        self.w.show() 
        
    def send_command(self,Command):
#        print Device, Command
        if System == "Sonos":
            if sn.set_device(player=Device, command=Command):
                self.parent.close()
        elif System == "XS1":
            if xs1.set_device(Device, Command):
                self.parent.close()
        elif System == "Hue":
            if hue.set_device(Device, Command):
                self.parent.close()
        elif System == "TV":
            if tv.set_device(Device, Command):
                self.parent.close()
        elif System == "Satelliten":
            if sat.set_device(Device, Command):
                self.parent.close()     
         
    def execute_on_server(self, szene):
        commado = {'Szene':str(szene)}
        csocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        csocket.sendto(str(commado),(constants.udp_.SERVER,constants.udp_.broadPORT))                

class MyPopup(QtGui.QMainWindow):
    def __init__(self, parent=None, Text="Test"):
        #super(MyPopup, self).__init__(parent)
        global System
        QtGui.QWidget.__init__(self)
        self.showMaximized()
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
        
        self.scrollLayout.setContentsMargins(50, 50, 50, 50)
#        self.scrollLayout.setVerticalSpacing(50)


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
        elif Text in sat_devs:
            System = "Satelliten"
            for item in sat.list_commands(Text):
                self.scrollLayout.addRow(Buttn(self,str(item),"Command"))                 
        self.scrollLayout.setRowHeight(1,50)
    #def paintEvent(self, e):
        #self.scrollLayout.addRow(Test("test"))
        #pass
        #dc = QtGui.QPainter(self)
        #dc.drawLine(0, 0, 100, 100)
        #dc.drawLine(100, 0, 0, 100)

class AEPopup(QtGui.QMainWindow):
    def __init__(self, parent=None, Text="Alarm & Events"):
        super(AEPopup, self).__init__(parent)
        #self.parent = parent
        QtGui.QWidget.__init__(self)
        self.showMaximized()
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
        
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setGeometry(QtCore.QRect(200, 10, 91, 24))
        self.pushButton.setObjectName("AESUpButton")
        self.pushButton.clicked.connect(self.AESrefresh)  
        self.mainLayout.addWidget(self.pushButton) 
        
        AEs = aes.alarm_events_read(unacknowledged=False, prio=0, time=24*60)
        for Event in AEs:
            self.scrollLayout.addRow(AESText(self,Event)) 
        self.newestEvent = AEs[0].get('Date')            

    def startAutoUpdate(self):
        while running:
            self.AESrefresh()
            time.sleep(5)

    def AESrefresh(self):
        global newestEvent
        AEs = aes.alarm_events_read(unacknowledged=False, prio=0, time=2*60)
        for Event in reversed(AEs):
            #print Event.get('Date') , self.newestEvent
            if Event.get('Date') > self.newestEvent:
                #currentRowCount = self.scrollLayout.rowCount()
                self.scrollLayout.insertRow(0,AESText(self,Event))
        self.newestEvent = AEs[0].get('Date')            
#        AESrefreshT = Timer(5, self.AESrefresh, [])
#        AESrefreshT.start()                  

class AESText(QtGui.QWidget):
    def __init__( self ,parent, Event):
      super(AESText, self).__init__(parent)
      colorcode = {0:"palegreen",1:"orange",2:"orange",3:"orange",4:"red",5:"red",6:"red"}
      #self.parent = parent
      self.lbldate = QtGui.QLabel()
      self.lbldate.setText(str(Event.get('Date')))
      self.lbldate.setGeometry(QtCore.QRect(0, 0, self.lbldate.width(), 10))
      self.lbl = QtGui.QLabel()
      self.lbl.setText(Event.get('Description'))
      self.lbl.setGeometry(QtCore.QRect(1, 0, self.lbl.width(), 60))      
      self.lblAck = QtGui.QLabel()
      self.lblAck.setText(str(Event.get('Acknowledged')))
      self.lblAck.setGeometry(QtCore.QRect(2, 0, 50, 50))       
      layout = QtGui.QHBoxLayout()
      layout.addWidget(self.lbldate)        
      layout.addWidget(self.lbl) 
      layout.addWidget(self.lblAck) 
      layout.addStretch()
      layout.setStretchFactor(self.lbl, 99)
      self.setStyleSheet(str("background: "+colorcode.get(int(Event.get("Prio")))))
      self.setLayout(layout)

class MyGraphPopup(QtGui.QMainWindow):
    def __init__(self, parent, item):
            #super(MyGraphPopup, self).__init__(parent)
            #global System
            #QtGui.QWidget.__init__(self)
        
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
            #win.resize(1000,600)
        self.win.setWindowTitle('Homecontrol Graph')
        self.win.showMaximized()#showFullScreen()
        
        self.xaxis = TimeAxisItem('bottom')
        self.yaxis = pg.AxisItem('right')
        
        graph = np.array(mdb_read_table_column_filt(db='HIS_inputs',column='Value', filt=item, amount=5000, order="desc",exact=True))
        timerange = mdb_read_table_column_filt(db='HIS_inputs',column='Date', filt=item, amount=5000, order="desc",exact=True)
        time = np.array(timerange)
            #graph = np.array([0,1,2,3,4,3,2,1])#np.random.normal(size=100)
            #time = np.array([0,1,2,3,4,3,2,1])
        plot = self.win.addPlot(title="Whatever",axisItems={'bottom':self.xaxis,'right':self.yaxis},x=time, y=graph)  
        plot.setXRange(timerange[0], timerange[-3000], padding=0)
        if 'A00' in item:
            plot.setYRange(-10,40)
        elif 'TE' in item:
            plot.setYRange(15,30)        
#        jetzt = mdb_read_table_column_filt(db='HIS_inputs',column='Date', filt=item, amount=1, order="desc")
#        fruher = mdb_read_table_column_filt(db='HIS_inputs',column='Date', filt=item, amount=1000, order="desc")[999]
#        self.win.setXRange(fruher,jetzt)
            #curve = p1.plot()

class MySZTreePopup(QtGui.QMainWindow):
    def __init__(self, parent, item):
        #super(MyGraphPopup, self).__init__(parent)
        #global System
        #QtGui.QWidget.__init__(self)
        
        #self.t = ParameterTree()
        #self.sz=Szenen_tree("TV")
        #self.t.setParameters(self.sz.p, showTop=False)
        #self.t.setWindowTitle('Szenen Setup:')
        #t2 = ParameterTree()
        #t2.setParameters(p, showTop=False)
        
        self.win = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(layout)
        self.layout.addWidget(QtGui.QLabel(""), 0,  0, 1, 2)
        #layout.addWidget(t2, 1, 1, 1, 1)
        self.win.show()
        self.win.resize(800,800)        
        


class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [QDateTime(1970,1,1,1.0,0).addSecs(value).toString('yyyy-MM-dd hh:mm') for value in values]
    
                 
running = True
app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('/home/christoph/spyder/sz/Controlroom.png'))
myWidget = Main()
if constants.gui_.KS:
    exectext = 'unclutter -idle 0.01 &'
#    os.system(exectext)
#    exectext = 'sudo echo 130 > /sys/class/backlight/rpi_backlight/brightness'
#    os.system(exectext)
    myWidget.showFullScreen()
myWidget.setGeometry(QRect(0, 0, 800, 540))
myWidget.show()
app.exec_() 
running = False