#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 18:24:21 2017

@author: christoph
"""

import constants
import MySQLdb as mdb

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.popup import Popup
import pandas as pd
import numpy as np
 
"""
Tree view with all actors in house
selected actor shows featurs:
    - Designation
    - Description
    - Type
    - if Satellite
        - show satellite entries
 
Designation changes should indicate where else a setting needs to be changed
 
add actor
"""
 
stockwerke_dict = {'Vm1':'Keller','V00':'Erdgeschoss','V01':'1. Stock','V02':'2. Stock',
                   'A00':'Draussen', 'VIR':'Virtuell'}

zim_dict = {'ZIM':'Zimmer',
            'WOH':'Wohnzimmer',
            'KUE':u'Küche',
            'BAD':u'Badezimmer/Toilette',
            'SCH':'Schlafzimmer',
            'FLU':'Flur',
            'BUE':u'Büro',
            'KID':'Kinderzimmer',
            'ESS':'Esszimmer',
            
            'KOM':'Kommunikation',
            'SSH':'SecureShell',
            'BEW':'Bewohner'}

furn_dict = {'SCA':'Scanner',
             'ADV':'Advent',
             'EIN':'Eingang',
             'STV':'Stromversorgung', 
             'RUM':'Raum', 
             'DEK':'Decke', 
             'SRA':'Schrank',
             'SOF':'Sofa', 
             'TUE':u'Tür', 
             'SEV':'Server', 
             'PFL':'Pflanzen',
             'BET':'Bett',
             
             
             'RUT':'Router',
             'SAT':'Satellite'}

types = ['XS1','SATELLITE','ZWave', 'SONOS', 'HUE']
 
con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)

def exce_msql(commando):
    with con:
        cur = con.cursor()
        sql = commando
        cur.execute(sql)        
    

class MyTreeView(TreeView):
 
    def __init__(self, **kwargs):
        super(MyTreeView, self).__init__(**kwargs)
        self.callback = None
 
    def select_node(self, node):
        '''Select a node in the tree.
        '''
#        if node.no_selection:
#            return
#        if self._selected_node:
#            self._selected_node.is_selected = False
#        node.is_selected = True
#        self._selected_node = node
        super(MyTreeView, self).select_node(node)
        if self.callback!=None:
            self.callback(node)
 
    def set_callback(self, call):
        self.callback = call
 
class ActorScreen(GridLayout):
 
    @staticmethod
    def get_description(obj_id):
        dictionaries = [stockwerke_dict, zim_dict, furn_dict]
        if len(obj_id) > 3:
            obj_id = obj_id[:3]
        for dicit in dictionaries:
            if obj_id in dicit:
                return dicit[obj_id]# + counter
 
    def __init__(self, **kwargs):
        super(ActorScreen, self).__init__(**kwargs)
        self.__events__ = ('select_node')
        self.cols = 2
        self.tv = MyTreeView(hide_root=True)
        self.tv.set_callback(self.node_change)
        self.build_tree()
        self.add_widget(self.tv)
        self.det_screen = DetailsScreen(self)
        self.add_widget(self.det_screen)
 
    def build_tree(self):
        self.szenen = pd.read_sql('SELECT * FROM set_Szenen', con=con)
        self.sats = pd.read_sql('SELECT * FROM set_satellites', con=con)
        for node in self.tv.iterate_all_nodes():
            self.tv.remove_node(node)
        first_level = self.tv.add_node(TreeViewLabel(text='Veltheim', is_open=True))
        for aktor in sorted(self.szenen.columns):
            level = aktor[:3]
            if level[:1] == 'V':
                level_obj = self.get_sub_object(first_level, level)
                raum = aktor[3:7]
                raum_obj = self.get_sub_object(level_obj, raum)
                furni = aktor[7:11]
                furni_obj = self.get_sub_object(raum_obj, furni)
                self.add_device(furni_obj, aktor)
                
    
    def add_sub_object(self, top_object, sub_object_Id):
        name = None
        for liste in [stockwerke_dict, zim_dict, furn_dict]:
            if sub_object_Id[:3] in liste:
                name = liste[sub_object_Id[:3]]
                break
 
        sub_object = TreeViewLabel(text=name)
        self.tv.add_node(sub_object, top_object)
        return sub_object
 
    def get_sub_object(self, top_object, sub_object_Id):
        for obj in top_object.nodes:
            if obj.id == sub_object_Id:
                return obj
        desc = self.get_description(sub_object_Id)
        child_node = TreeViewLabel(text=desc, id=sub_object_Id)
        return self.tv.add_node(child_node, top_object)
 
    def add_device(self, top_object, device):
        device_desc = self.szenen.get_value(4, device)
        if device_desc == None:
            device_desc = device
        child_node = TreeViewLabel(text=device_desc, id=device)
        self.tv.add_node(child_node, top_object)
 
    @staticmethod
    def r_none(value):
        if value == None:
            return ""
        else:
            return str(value)
    
    def node_change(self, node):
        if node.id in self.szenen.columns:
            device_desc = self.szenen.get_value(4, node.id)
            device_type = self.szenen.get_value(0, node.id)
            self.det_screen.designation.text = node.id
            self.det_screen.description.text = self.r_none(device_desc)
            self.det_screen.mainbutton.text = self.r_none(device_type)
            self.det_screen.hks = node.id
            if device_type in ['SATELLITE']:
                ind = self.sats.loc[self.sats['Name'] == node.id].index
                self.det_screen.IP_add.text = self.r_none(self.sats.get_value(ind[0], 'IP'))
                self.det_screen.port_bc.text = self.r_none(self.sats.get_value(ind[0], 'PORT'))
                self.det_screen.username.text = self.r_none(self.sats.get_value(ind[0], 'USER'))
                self.det_screen.port_bid.text = self.r_none(self.sats.get_value(ind[0], 'BiPORT'))
                self.det_screen.password.text = self.r_none(self.sats.get_value(ind[0], 'PASS'))
                self.det_screen.table.text = self.r_none(self.sats.get_value(ind[0], 'command_set'))
            else:
                self.det_screen.IP_add.text = ''
                self.det_screen.port_bc.text = ''
                self.det_screen.username.text = ''
                self.det_screen.port_bid.text = ''
                self.det_screen.password.text = ''
                self.det_screen.table.text = ''              
 
 
class DetailsScreen(GridLayout):
 
    def __init__(self, mainview, **kwargs):
        super(DetailsScreen, self).__init__(**kwargs)
        self.cols = 2
        self.hks = None
        self.mainview = mainview
#        self.orientation='vertical'
 
        # Designation
        self.add_widget(Label(text='Designation'))
        self.designation = TextInput(multiline=False)
        self.designation.text = ''
        self.add_widget(self.designation)
 
        # Description
        self.add_widget(Label(text='Description'))     
        self.description = TextInput(multiline=False)
        self.description.text = ''
        self.add_widget(self.description)
 
        # Dropdown for Type
        self.add_widget(Label(text='Type'))
        self.dropdown_type = DropDown()
        for item in types:       
            btn = Button(text=item, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown_type.select(btn.text))
            self.dropdown_type.add_widget(btn)
        self.mainbutton = Button(text='')#, size_hint=(None, None))
        self.mainbutton.bind(on_release=self.dropdown_type.open)
        self.dropdown_type.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.add_widget(self.mainbutton)
 
        # Save Button
#        self.save_device = Button(text='Save')
#        self.add_widget(self.save_device)
 
        ''' Satellite Settings '''
        # IP
        self.add_widget(Label(text='IP'))
        self.IP_add = TextInput(multiline=False)
        self.IP_add.text = ''
        self.add_widget(self.IP_add)
 
        # Port Broadcast
        self.add_widget(Label(text='Broadcast Port'))
        self.port_bc = TextInput(multiline=False)
        self.port_bc.text = ''
        self.add_widget(self.port_bc)       
 
        # Port bidirect
        self.add_widget(Label(text='Bidirect Port'))
        self.port_bid = TextInput(multiline=False)
        self.port_bid.text =  ''
        self.add_widget(self.port_bid)       
 
        # Username
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.username.text = ''
        self.add_widget(self.username)       
 
        # Passwort
        self.add_widget(Label(text='Password'))
        self.password = TextInput(multiline=False)
        self.password.text = ''
        self.add_widget(self.password)   
 
        # Table
        self.add_widget(Label(text='Table'))
        self.table = TextInput(multiline=False)
        self.table.text = ''
        self.add_widget(self.table)   
 
        # Save Button
        self.save_sat = Button(text='Save')
        self.add_widget(self.save_sat)
        self.save_sat.bind(on_press=self.btn_callback)
 
        # New Button
        self.new = Button(text='New')
        self.add_widget(self.new)
        self.new.bind(on_press=self.new_btn_callback)
        
        # Delete Button
        self.delete = Button(text='Delete')
        self.add_widget(self.delete)     
        self.delete.bind(on_press=self.del_btn_callback)
        
        # Update Button
        self.update = Button(text='Update')
        self.add_widget(self.update)     
        self.update.bind(on_press=lambda x:self.mainview.build_tree())
 
    def del_btn_callback(self, instance):
        content = BoxLayout()
        content.orientation='vertical'
        content.add_widget(Label(text='Delete %s?' %(self.hks)))
        yes_btn = Button(text='Yes delete')
        content.add_widget(yes_btn)
        popup = Popup(title='Test popup',
                      content=content,
                      size_hint=(None, None), size=(400, 400))
        yes_btn.bind(on_press=lambda btn: self.confirm_buttn_callback(popup))
        popup.open()
        
    def confirm_buttn_callback(self, parent):
        parent.dismiss()
        exce_msql("ALTER TABLE `Steuerzentrale`.`set_Szenen` DROP COLUMN `%s`;" % (self.hks))
        print('deleted')
        self.mainview.build_tree()
    
    def btn_callback(self, instance):
        print(self.hks)
        if self.hks <> self.designation.text:
            exce_msql("ALTER TABLE `Steuerzentrale`.`set_Szenen` CHANGE COLUMN `%s` `%s` TEXT NULL DEFAULT NULL;" % (self.hks, self.designation.text))
        exce_msql("UPDATE `Steuerzentrale`.`set_Szenen` SET `%s`='%s' WHERE `Id`='5';" % (self.designation.text, self.description.text))
        exce_msql("UPDATE `Steuerzentrale`.`set_Szenen` SET `%s`='%s' WHERE `Id`='1';" % (self.designation.text, self.mainbutton.text))
        if self.mainbutton.text == 'SATELLITE':
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `IP`='%s' WHERE `Name`='%s';" % (self.IP_add.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `PORT`='%s' WHERE `Name`='%s';" % (self.port_bc.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `BiPORT`='%s' WHERE `Name`='%s';" % (self.port_bid.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `USER`='%s' WHERE `Name`='%s';" % (self.username.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `PASS`='%s' WHERE `Name`='%s';" % (self.password.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `command_set`='%s' WHERE `Name`='%s';" % (self.table.text, self.designation.text))
            
        if self.hks <> self.designation.text and self.mainbutton.text == 'SATELLITE':
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `Name`='%s' WHERE `Name`='%s';" % (self.designation.text, self.hks))
        self.mainview.build_tree()

    def new_btn_callback(self, instance):
        print(self.hks)
        exce_msql("ALTER TABLE `Steuerzentrale`.`set_Szenen` ADD COLUMN `%s` TEXT NULL AFTER `%s`;" % (self.designation.text, self.hks))
        exce_msql("UPDATE `Steuerzentrale`.`set_Szenen` SET `%s`='%s' WHERE `Id`='5';" % (self.designation.text, self.description.text))
        exce_msql("UPDATE `Steuerzentrale`.`set_Szenen` SET `%s`='%s' WHERE `Id`='1';" % (self.designation.text, self.mainbutton.text))
        if self.mainbutton.text == 'SATELLITE':
            exce_msql("INSERT INTO `Steuerzentrale`.`set_satellites` (`Name`) VALUES ('%s');" % (self.designation.text))
            
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `IP`='%s' WHERE `Name`='%s';" % (self.IP_add.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `PORT`='%s' WHERE `Name`='%s';" % (self.port_bc.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `BiPORT`='%s' WHERE `Name`='%s';" % (self.port_bid.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `USER`='%s' WHERE `Name`='%s';" % (self.username.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `PASS`='%s' WHERE `Name`='%s';" % (self.password.text, self.designation.text))
            exce_msql("UPDATE `Steuerzentrale`.`set_satellites` SET `command_set`='%s' WHERE `Name`='%s';" % (self.table.text, self.designation.text))
   
        self.mainview.build_tree()
    
# ALTER TABLE `Steuerzentrale`.`set_Szenen` DROP COLUMN `V00FLU1RUM1PC01`;
    
class MyApp(App):
 
    def build(self):
        return ActorScreen()
 
 
if __name__ == '__main__':
    MyApp().run()
    con.close()
 