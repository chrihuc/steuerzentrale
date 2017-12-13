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

class Room(object):
    
    def __init__(self, name):
        self.name = name
        self._set_temp = None
        self._act_temp = None
        self._actuator_temp = None
        self._actuator_set = None
        
        self.act_hks = name[:11] + 'TE' + name[13:]
        self.actu_t_hks = name[:11] + 'AT' + name[13:]
        self.actu_s_hks = name[:11] + 'SA' + name[13:]
        
    def __str__(self):
        varias = (self._set_temp, self._act_temp, self._actuator_temp, self._actuator_set)
        return str([str(i) for i in varias])
        
    @property
    def set_temp(self):
        return self._set_temp
    
    @set_temp.setter
    def set_temp(self, value):
        self._set_temp = float(value)
    
    @property
    def act_temp(self):
        return self._act_temp
    
    @act_temp.setter
    def act_temp(self, value):
        self._act_temp = float(value)
        
    @property
    def actuator_temp(self):
        return self._actuator_temp
    
    @actuator_temp.setter
    def actuator_temp(self, value):
        self._actuator_temp = float(value)
        
    @property
    def actuator_set(self):
        return self._actuator_set
    
    @actuator_set.setter
    def actuator_set(self, value):
        if value == False:
            raise ValueError('Setting not existing')
        self._actuator_set = value

    def update_setpoint(self):
        self._actuator_set = self._actuator_temp + (self._set_temp - self._act_temp)
        return self._actuator_set
    
class TempController(object):
    
    zones = []
    rooms = []
    cylcetime = 60
    running = False
    
    def __init__(self):
        pass
    
    @classmethod
    def get_zones(cls):
        cls.zones = []
        all_sets = msqc.settings_r()
        for setting in all_sets:
            if setting[11:13] == 'ST':
                cls.zones.append(setting)
    
    @classmethod
    def init_rooms(cls):
        cls.get_zones()
        for zone in cls.zones:
            new_room = Room(zone)
            new_room.set_temp = msqc.setting_r(zone)
            new_room.act_temp = msqc.setting_r(new_room.act_hks)
            new_room.actuator_temp = msqc.setting_r(new_room.actu_t_hks)
            cls.rooms.append(new_room)
   
    @classmethod
    def update_rooms(cls):
        for room in cls.rooms:
            room.set_temp = msqc.setting_r(room.name)
            room.act_temp = msqc.setting_r(room.act_hks)
            room.actuator_temp = msqc.setting_r(room.actu_t_hks)
            room.update_setpoint()
            toolbox.log(room.actu_s_hks, room.actuator_set, level=1)
            payload = {'Device':room.actu_s_hks,'Command':room.actuator_set}
            toolbox.communication.send_message(payload, typ='SetDevice')
    
    @classmethod
    def update_setpoints(cls):
        for room in cls.rooms:
            room.update_setpoint()
            print room.actuator_set
    
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
        cls.init_rooms()
        cls.running = True
        t = threading.Thread(target=cls.cycling)
        t.start()
    
    @classmethod
    def start(cls):
        cls.init_rooms()
        cls.running = True
        cls.cycling()
    
#TempController.get_zones()