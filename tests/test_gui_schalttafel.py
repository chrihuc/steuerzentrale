# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 11:57:40 2017

@author: 212505558
1."""

stockwerke_dict = {'Vm1':'Keller','V00':'Erdgeschoss','V01':'1. Stock','V02':'2. Stock',
                   'A00':'Draussen'}
zim_dict = {'ZIM':'Zimmer','WOH':'Wohnzimer','KUE':u'Küche','BAD':u'Badezimmer/Toilette',
            'SCH':'Schlafzimmer','FLU':'Flur','BUE':u'Büro','ESS':'Esszimmer'}
furn_dict = {'SCA':'Scanner','ADV':'Advent','KID':'Kinderzimmer','EIN':'Eingang',
             'STV':'Stromversorgung', 'RUM':'Raum', 'DEK':'Decke', '':''}

class TreeInputsDevices(object):
    def __init__(self):
        #self.inputs = mdb_get_table(db='cmd_inputs')
        self.inputs = ['Vm1ZIM1RUM1DI01', 'V00WOH1RUM1HE01']
        self.params = []        
        self.set_paratree()

    def add_sub_object(self, top_object, sub_object_Id):
        name = None
        for liste in [stockwerke_dict, zim_dict, furn_dict]:
            if sub_object_Id[:3] in liste:
                name = liste[sub_object_Id[:3]]
                break
        
        sub_object = {'name': name, 'type': 'group', 'expanded': True, 
                             'Id':sub_object_Id, 'children':[]}
        top_object['children'].append(sub_object)
        return sub_object
        
    def get_sub_object(self, top_object, sub_object_Id):
        for obj in top_object['children']:
            if obj['Id'] == sub_object_Id:
                return sub_object_Id
        return self.add_sub_object(top_object, sub_object_Id)

    def add_device(self, top_object, device):
        
        dev_obj = {'name': device, 'type': 'str', 'expanded': True, 'Id':device} 
        top_object['children'].append(dev_obj)
    
    def set_paratree(self):
        # top level floors
        top_level = {'name': u'Eingänge', 'type': 'group', 'expanded': True, 'children':[]}
#        for floor in stockwerke_dict:
#            floor_obj = {'name': stockwerke_dict[floor], 'type': 'group', 'expanded': True, 
#                         'Id':floor}
#            top_level['children'].append(floor_obj)
        for aktuator in sorted(self.inputs):
            level = aktuator[:3]
            level_obj = self.get_sub_object(top_level, level)
            raum = aktuator[3:7]
            raum_obj = self.get_sub_object(level_obj, raum)
            furni = aktuator[7:11]
            furni_obj = self.get_sub_object(raum_obj, furni)
            device = aktuator[11:]
            self.add_device(furni_obj, aktuator)
           
        self.params.append(top_level)
                
test = TreeInputsDevices()
exam = test.params
print "ende"

