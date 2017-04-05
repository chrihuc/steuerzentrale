# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 11:57:40 2017

@author: chuckle
1."""

#test teil
inputs = [{'Name':'Vm1ZIM1RUM1DI01', 'Description':'Decke'}, 
          {'Name':'V00WOH1RUM1HE01', 'Description':'Decke'}]

#normaler code

stockwerke_dict = {'Vm1':'Keller','V00':'Erdgeschoss','V01':'1. Stock','V02':'2. Stock',
                   'A00':'Draussen'}
zim_dict = {'ZIM':'Zimmer','WOH':'Wohnzimmer','KUE':u'Küche','BAD':u'Badezimmer/Toilette',
            'SCH':'Schlafzimmer','FLU':'Flur','BUE':u'Büro','ESS':'Esszimmer'}
furn_dict = {'SCA':'Scanner','ADV':'Advent','KID':'Kinderzimmer','EIN':'Eingang',
             'STV':'Stromversorgung', 'RUM':'Raum', 'DEK':'Decke', '':''}

class TreeInputsDevices(object):
    def __init__(self, inputs):
        #self.inputs = mdb_get_table(db='cmd_inputs')
        self.params = []        
        self.set_paratree(inputs)

    def add_sub_object(self, top_object, sub_object_Id):
        name = None
        for liste in [stockwerke_dict, zim_dict, furn_dict]:
            if sub_object_Id[:3] in liste:
                name = liste[sub_object_Id[:3]]
                break
        
        sub_object = {'title': name, 'type': 'group', 'expanded': True, 
                             'name':sub_object_Id, 'children':[]}
        top_object['children'].append(sub_object)
        return sub_object
        
    def get_sub_object(self, top_object, sub_object_Id):
        for obj in top_object['children']:
            if obj['name'] == sub_object_Id:
                return sub_object_Id
        return self.add_sub_object(top_object, sub_object_Id)

    def add_device(self, top_object, device):
        device_id = device['Name']
        device_desc = device['Description']
        dev_obj = {'title': device_desc, 'type': 'str', 'expanded': True, 'name':device_id} 
        top_object['children'].append(dev_obj)
    
    def set_paratree(self, inputs):
        # top level floors
        top_level = {'name': u'Eingänge', 'type': 'group', 'expanded': True, 'children':[]}
#        for floor in stockwerke_dict:
#            floor_obj = {'name': stockwerke_dict[floor], 'type': 'group', 'expanded': True, 
#                         'Id':floor}
#            top_level['children'].append(floor_obj)
        for aktuator in sorted(inputs):
            aktuator_id = aktuator['Name']
            level = aktuator_id[:3]
            level_obj = self.get_sub_object(top_level, level)
            raum = aktuator_id[3:7]
            raum_obj = self.get_sub_object(level_obj, raum)
            furni = aktuator_id[7:11]
            furni_obj = self.get_sub_object(raum_obj, furni)
            device = aktuator_id[11:]
            self.add_device(furni_obj, aktuator)
           
        self.params.append(top_level)
        
class TreeInputDevice(object):
    def __init__(self, device):
        self.params = []
        self.set_paratree(device)

    def set_paratree(self, device_name):
        _szn_lst = []
        for device in inputs:
            if device['Name'] == device_name:
                break
        top_level = {'name': device_name, 'type': 'group', 'expanded': True, 'children':[]}
        kinder = top_level['children']
        for feature, value in device.iteritems():
            if feature in ['Logging','Setting','Doppelklick']:
                kinder.append({'name':feature, 'type': 'bool', 'value':bool(value)})
            elif feature in ['Description']:
                kinder.insert(0, {'name':feature, 'title':'Beschreibung', 'type': 'str',
                                  'value':value})
            elif feature in ['Immer', 'Wach', 'Wecken', 'Schlafen', 'Schlummern', 'Leise', 
                             'AmGehen', 'Gegangen', 'Abwesend', 'Urlaub', 'Besuch', 'Doppel',
                             'Dreifach']:
                kinder.append({'name':feature, 'type': 'list', 'value':value, 
                               'values':sorted(_szn_lst)}) 
            elif feature in ['Id']:
                pass
            else:
                kinder.append({'name':feature, 'type': 'str', 'value':value})
        self.params.append(top_level)
    
test = TreeInputsDevices(inputs)
exam = test.params
test.set_paratree(inputs)
test_dev = TreeInputDevice('V00WOH1RUM1HE01')
pra = test_dev.params
print "ende"

