#!/usr/bin/python
# -*- coding: utf-8 -*-

import constants

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights

import sys
from PyQt4.QtGui import *
from PyQt4.Qt import *

class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)

class Test(QWidget):
  def __init__( self, parent=None):
      super(Test, self).__init__(parent)

      self.pushButton = QPushButton('I am in Test widget')

      layout = QHBoxLayout()
      layout.addWidget(self.pushButton)
      self.setLayout(layout)

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.sn = sonos()
        self.xs1 = myezcontrol(constants.xs1_.IP)
        self.hue = hue_lights()
        self.dev_mod = None
        self.cmd_mod = None
        self.mode = None
        self.initUI()
        
    def initUI(self):
        global dev_mod
        global cmd_mod
        QToolTip.setFont(QFont('SansSerif', 10))
        
        #self.setToolTip('This is a <b>QWidget</b> widget')
        
        dev_lst = QListView(self)
        dev_lst.setWindowTitle('Devices')
        dev_lst.move(0, 50) 
        dev_lst.setMinimumSize(200, 400)
            
        self.dev_mod = QStandardItemModel(dev_lst)
        
        dev_lst.setModel(self.dev_mod)
        
        cmds_lst = QListView(self)
        cmds_lst.setWindowTitle('Devices')
        cmds_lst.move(260, 50) 
        cmds_lst.setMinimumSize(200, 400)
            
        self.cmd_mod = QStandardItemModel(cmds_lst)

        cmds_lst.setModel(self.cmd_mod)
        
        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)        
        
        self.mainLayout.addWidget(self.scrollArea)
        
        sns = QPushButton('Sonos', self)
        #sns.setToolTip('This is a <b>QPushButton</b> widget')
        sns.resize(sns.sizeHint())
        sns.clicked.connect(self.addWidget)
        
        xs1 = QPushButton('XS1', self)
        #xs1.setToolTip('This is a <b>QPushButton</b> widget')
        xs1.resize(xs1.sizeHint())
        xs1.clicked.connect(self.xs1_clicked)        
        xs1.move(70, 0)  
        
        hue = QPushButton('Hue', self)
        #xs1.setToolTip('This is a <b>QPushButton</b> widget')
        hue.resize(hue.sizeHint())
        hue.clicked.connect(self.hue_clicked)        
        hue.move(140, 0) 
        
        btn = QPushButton('Execute', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(100,100)#btn.sizeHint())
        btn.clicked.connect(self.btn_clicked)        
        btn.move(600, 20)       
        
        self.setGeometry(700, 500, 750, 450)
        self.setWindowTitle('Kontrollraum')    
        self.show()
        
    def set_liste(self, devices, commands):
        global dev_mod
        global cmd_mod   
        self.dev_mod.clear()
        self.cmd_mod.clear()
        for dev in devices:
            item = QStandardItem(dev)
            item.setCheckable(True)
            self.dev_mod.appendRow(item)  
        for cmd in commands:
            item = QStandardItem(str(cmd))
            item.setCheckable(True)
            self.cmd_mod.appendRow(item)            
        
        
    def addWidget(self):
        self.scrollLayout.addRow(Test())        
        
    def sns_clicked(self):
        tst = QPushButton('test', self)
        tst.resize(tst.sizeHint())
        tst.clicked.connect(self.hue_clicked)        
        tst.move(600, 140)          
        devs = self.sn.list_devices()
        cmds = self.sn.list_commands() 
        global mode
        self.mode = "Sonos"
        self.set_liste(devs, cmds)
       
        
    def xs1_clicked(self):
        devs = self.xs1.list_devices()
        cmds = self.xs1.list_commands() 
        global mode
        self.mode = "XS1"
        self.set_liste(devs, cmds)   
        
    def hue_clicked(self):
        devs = self.hue.list_devices()
        cmds = self.hue.list_commands() 
        global mode
        self.mode = "Hue"
        self.set_liste(devs, cmds)         
        
    def set_popup(self):
        self.w = MyPopup()
        self.w.setGeometry(QRect(100, 100, 100, 100))
        self.w.show()        
        
    def btn_clicked(self):
        commds = []
        for i in range(self.cmd_mod.rowCount()):
            if self.cmd_mod.item(i).checkState():
                commds.append(self.cmd_mod.item(i).text())
        for i in range(self.dev_mod.rowCount()):
            if self.dev_mod.item(i).checkState():
                for cmmd in commds:
                    print self.dev_mod.item(i).text(), cmmd
                    if self.mode == "Sonos":
                        if self.sn.set_device(player=self.dev_mod.item(i).text(), command=cmmd):
                            self.set_popup()
                    elif self.mode == "XS1":
                        self.xs1.set_device(self.dev_mod.item(i).text(), cmmd)   
                    elif self.mode == "Hue":
                        self.hue.set_device(self.dev_mod.item(i).text(), cmmd)                          
        
def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
