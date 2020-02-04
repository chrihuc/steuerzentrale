#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:56:36 2017

@author: christoph
"""

import time
import threading

import constants
from tools import toolbox

from database import mysql_connector as msqc

def myround(x, base=.5):
    return (base * round(float(x)/base))

class Zone(object):
    
    def __init__(self, Id):
        self.Id = Id
        self._set_temp = None
        self._act_temp = None
        self._offset = 0        
        self._actuator_temp = None
        self._actuator_set = None
        
        self._inputs = None
        self._reference = None
        self._actuator_temp_hks = None
        self._output = None
        self.enabled = False
        
    def __str__(self):
        varias = (self._set_temp, self._act_temp, self._actuator_temp, self._actuator_set)
        return str([str(i) for i in varias])
        
    @property
    def inputs(self):
        return self._inputs
    
    @inputs.setter
    def inputs(self, value):
        try:
            if isinstance(eval(value), list):
                self._inputs = eval(value)
        except:
            pass

    def get_act_temp(self):
        counter = 0
        summ = 0.0
        for inpt in self._inputs:
            summ += float(msqc.get_input_value(inpt))
            counter += 1
        self._act_temp = summ/counter
        return self._act_temp
    
    @property
    def reference(self):
        return self._reference
    
    @reference.setter
    def reference(self, value):
        self._reference = value
    
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self, value):
        try:
            self._offset = float(value)
        except:
            pass
    
    def get_set_value(self):
        setting = msqc.get_actor_value(self._reference)
        if setting in ['Off', 'off', 'Man', 'man', 'manual']:
            self._set_temp = self._act_temp
            self.enabled = False
        else:
            self._set_temp = float(setting)
            self.enabled = True
        return self._set_temp
        
    def get_actuator_temp(self):
        self._actuator_temp = float(msqc.get_input_value(self._actuator_temp_hks))
        return self._actuator_temp
        
    @property
    def actuator_temp_hks(self):
        return self._actuator_temp_hks
    
    @actuator_temp_hks.setter
    def actuator_temp_hks(self, value):
        self._actuator_temp_hks = value
        
    @property
    def output(self):
        return self._output
    
    @output.setter
    def output(self, value):
        self._output = value

    def update_setpoint(self):
        self._actuator_set = self._actuator_temp + (self._set_temp - self._act_temp) + self._offset
#        print('Temp Control', self._actuator_temp, self._set_temp, self._act_temp)
        # rounding dependend on system
        self._actuator_set = myround(self._actuator_set)
#        print('Temp Set', self._actuator_set)
        return self._actuator_set
    
    def cycle(self):
        self.get_act_temp()
        self.get_set_value()
        self.get_actuator_temp()
        self.update_setpoint()
        if self.enabled:
            payload = {'Device':self._output,'Command':self._actuator_set}
            toolbox.communication.send_message(payload, typ='SetDevice')
        return self._actuator_set
    
class TempController(object):
    
    zones = []
    cylcetime = 2*60
    running = False
    
    def __init__(self):
        pass
    
    @classmethod
    def load_zones(cls):
        cls.zones = []
        sql_zones = msqc.mdb_get_table(constants.sql_tables.TempControl.name)
        for zone in sql_zones:
            new_zone = Zone(zone['Id'])
            new_zone.inputs = zone['inputs']
            new_zone.reference = zone['ref_value']
            new_zone.offset = zone['offset']
            new_zone.actuator_temp_hks = zone['actor_reading']
            new_zone.output = zone['output']
            cls.zones.append(new_zone)
   
    @classmethod
    def update_rooms(cls):
        for room in cls.zones:
            room.cycle()
    
    
    @classmethod
    def stop(cls):
        cls.running = False
        
    @classmethod
    def cycling(cls):
        while cls.running and constants.run:
            cls.update_rooms()
            time.sleep(cls.cylcetime)
    
    @classmethod
    def start_thread(cls):
        cls.load_zones()
        cls.running = True
        t = threading.Thread(target=cls.cycling)
        t.start()
    
    @classmethod
    def start(cls):
        cls.load_zones()
        cls.running = True
        cls.cycling()
    
#TempController.get_zones()