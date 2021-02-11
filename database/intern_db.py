#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 05:52:12 2021

@author: christoph
"""

import json
from threading import Timer
import datetime
import decimal
import copy

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif  isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        result = 'not json serializable'
        try:
            result = eval(obj)
        except Exception as e:
            print('could not convert', obj, type(obj))
        return result
    return 'not json serializable' #TypeError ("Type %s not serializable" % type(obj))


def convert_to(string, targettype):
    result = None
    if not type(string) == str or (type(string) == targettype and targettype != str):
        return string
    if targettype == str:
        if len(string) > 0:
            result = string
    elif targettype == int:
        if len(string) > 0:
            result = int(string)
    elif targettype == float:
        if len(string) > 0:
            result = float(string)
    elif targettype == bool:
        if len(string) > 0:
            result = 'True' in string
    elif targettype == datetime.datetime:
        if len(string) > 0 and string != 'NULL':          
            if len(string) > len('2019-09-30T10:49:14'):
                if 'T' in string:
                    result = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f') #.%f
                else:
                    result = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')
            else:
                if 'T' in string:
                    result = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')  
                else:
                    result = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            result = None                    
    return result

class New_Element(object):
    
    def __init__(self, dbProps, props):#, Id, name, description):
        for key,val in props.items():
            for key2,val2 in dbProps.items():
                if key2.upper() == key.upper():
                    self.__dict__[key2] = val
                    break
        for key,val in dbProps.items():
            if not key in self.__dict__:
                self.__dict__[key] = val[0]
            
    def get_as_dict(self):
        result = {}
        for key, val in self.__dict__.items():
            result[key] = val
        return result
   
class DatabaseIntern(object):
    
    def __init__(self, props, filename=None):
        self.props    = props
        self.elements = []
        self.lock     = False
        self.datasets = 0
        self.filename = filename

    def new_value(self, name, value, ct=None, valid=True):
        result = [element for element in self.elements if name == element.Name]
        last_value = None
        if result:
            for el in result:
                last_value = el.Value
                el.Value = value
                el.time  = ct
                el.valid = valid
                
            return result, last_value
        else:
            element = New_Element(self.props, {'Name':name,'Value':value, 'HKS':name, 'Description':name, 'time':ct})
            max_id = self.get_max_id()
            if max_id:
                element.Id = max_id + 5
            else:
                element.Id = 1
            self.elements.append(element)
            return [element], last_value
    
    def new_trigger(self, Id):
        curEl = self.get_element_by_id(Id)
        newEl = copy.copy(curEl)
        max_id = self.get_max_id()
        newEl.Id = max_id + 5  
        self.elements.append(newEl)
        self.save_to_file()
    
    def new_item(self, props):
        result = [element for element in self.elements if props['Id'] == element.Id]    
        if result:
            return result
        else:
            if 'last_Value' in props:
                props['Value'] = props['last_Value']            
            for key, value in props.items():
#                for key2, value2 in self.props.items():
#                    if key.upper() == key2.upper() and key != key2:
#                        props[key2] = value
                if key in self.props:
                    props[key] = convert_to(value, self.props[key][1])
                     
            element = New_Element(self.props, props)
            self.elements.append(element)
            return [element]        
        
    def get_sorted_by(self, sort, reverse=False, filtby='', filtkey=''):
        elements = [element for element in self.elements]
        if filtby == 'Name':
            elements = [element for element in self.elements if filtkey in element.Name]
        if filtby == 'HKS':
            elements = [element for element in self.elements if filtkey in element.HKS]   
        if filtby == 'Description':
            elements = [element for element in self.elements if filtkey in element.Description]             
        return sorted(
            elements,
            key=lambda x: (getattr(x, sort) is None, str(getattr(x, sort))),
#            key=lambda x: getattr(x, sort) if getattr(x, sort) else 0,
            reverse=reverse)        
        
    def get_max_id(self):
        elements = [element for element in self.elements]
        t_list = sorted(elements,
            key=lambda x: getattr(x, 'Id'),
#            key=lambda x: getattr(x, sort) if getattr(x, sort) else 0,
            reverse=True)        
        if t_list:
            return t_list[0].Id
        else:
            return None        
    
    def del_element(self, Id):
        pos = None
        for idx, val in enumerate(self.elements):
            if val.Id == Id:
                pos = idx
                break
        if pos:
            del self.elements[pos]
        print('deleted')
    
    def get_element_by_id(self, Id):
        self.lock = True
        results = [i for i in self.elements if i.Id == Id]
        self.lock = False
        if len(results) > 0:
            return results[0]
        return False            
            
    def get_elements_by_name(self, Name):
        self.lock = True
        results = [i for i in self.elements if i.Name == Name]
        self.lock = False
        return results    
    
    def get_elements_by_hks(self, HKS):
        self.lock = True
        results = [i for i in self.elements if i.HKS == HKS]
        self.lock = False
        return results       
    
    def get_all_vals_as_dict(self):
        self.lock = True
        results = {i.HKS:i.Value for i in self.elements}
        self.lock = False
        return results 
    
    def periodic_save(self):
        thread_pt = Timer(60, self.periodic_save)
        thread_pt.start()    
        self.save_to_file()
        return True    
    
    def build(self, inputs_table):
        self.elements = []
        print('Lade Datensätze')
        if type(inputs_table) == dict:
            result = [self.new_item(item) for key, item in inputs_table.items()]
        else:
            result = [self.new_item(item) for item in inputs_table]
        self.datasets = len(self.elements)
        print('Input Datensätze geladen: ' + str(self.datasets))
        thread_pt = Timer(60, self.periodic_save)
        thread_pt.start()         
        return True            

    def get_as_list(self):
        liste = []
        for element in self.elements:
            liste.append(element.__dict__)
        return liste  

    def save_to_file(self):
        if self.filename and len(self.elements) > (self.datasets - 10):
            with open(self.filename, 'w') as fout:
                json.dump(self.get_as_list(), fout, default=json_serial) 
            self.datasets = len(self.get_as_list())
#            print('Input Datensätze geschrieben: ' + str(self.datasets))    
    
if __name__ == '__main__':
    properties = {'Val1':'Val1','Val2':'Val2','Val0':0,'ValNone':None}
    testel = New_Element(properties, {'Val1':'Value.1','Val2':2,'Val0':0})   
    print(testel.Val1)
#    print(testel['Val1'])
    properties = {'Id':None,'Name':'HKS','HKS':'HKS','Value':0,'time':None}
    InputsDB = DatabaseIntern(properties)
    res,_ = InputsDB.new_value('Inputs.3',23)
    print(res[0].Id)