#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:08:14 2017

@author: christoph
"""

    
import random
import time, datetime
from database import mysql_connector as msqc
from tools import toolbox
#from outputs import szenen

# TODO: class scene
# TODO: operationalize it, 
# TODO Tests split adress from hks

delay = 3 * 60
#scenes = szenen.Szenen()

class device(object):
    
    def __init__(self, name, an, aus, startt, endt, min_lux, perc_on, perc_off):
        self.name = name
        self.an = an
        self.aus = aus
        self.startt = startt
        self.endt = endt
        self.min_lux = min_lux
        self.perc_on = perc_on
        self.perc_off = perc_off
        self._inc_perc_on = perc_on
        self._inc_perc_off = perc_off
        self._increment = False
        self.status = False 
        self.last_switch = None
        self._latch_on = datetime.timedelta(0)
        self._latch_off = datetime.timedelta(0)
        
    @property
    def latch_on(self):
        return self._latch_on

    @latch_on.setter
    def latch_on(self, value): 
        self._latch_on = datetime.timedelta(0,value * 60)
    
    @property
    def latch_off(self):
        return self._latch_off

    @latch_off.setter
    def latch_off(self, value): 
        self._latch_off = datetime.timedelta(0,value * 60) 
        
    @property
    def increment(self):
        return self._increment
    
    @increment.setter
    def incrememt(self, value):
        self._increment = value
        
    def reset_increment(self):
        self._inc_perc_on = self.perc_on
        self._inc_perc_off = self.perc_off 
        
    def increase(self):
        if self._increment:
            self._inc_perc_on += self.perc_on
            self._inc_perc_off += self.perc_off        
    
    def switch(self):
        now = datetime.datetime.now()
        if self.startt > now.time() or now.time() > self.endt:
            # out of office hours
            if self.status:
                self.set_device(self.perc_off)
                self.last_switch = now
                return                
                
        lux = msqc.setting_r('V00WOH1RUM1HE01')
        if self.min_lux > 0 and self.min_lux > lux:
            # too bright
            return
                            
        if self.status:
            commando = self.aus
            wahrscheinlichkeit = self._inc_perc_off
        else:
            commando = self.an
            wahrscheinlichkeit = self._inc_perc_on       

        if self.last_switch != None:
            passed_time = now - self.last_switch
        else:
            passed_time = datetime.timedelta(24*60*60)
            
        if commando == self.aus:
            if self._latch_off > passed_time:
                wahrscheinlichkeit = 0
        else:
            if self._latch_on > passed_time:
                wahrscheinlichkeit = 0

        zufall = random.randint(1, 99) 
      
        if zufall in range(wahrscheinlichkeit):
            self.set_device(commando)
            self.last_switch = now
            self.reset_increment()
        else:
            self.increase()
        
    def set_device(self, commando):
#        scenes.threadSetDevice(self.name, commando)
        toolbox.log(self.name, commando, level=1)
        payload = {'Device':self.name,'Command':commando}
        toolbox.communication.send_message(payload, typ='SetDevice')
        self.status = not self.status
        
class anwesenheits_geist(object):
    
    def __init__(self, device_dictionary):
        self.dev_class_list = []
        self.running = False
        for iter_device in device_dictionary:
            name = iter_device
            # command to swith dev on
            an = device_dictionary[iter_device][0]
            # command to switch dev off
            aus = device_dictionary[iter_device][1]
            # start time for dev
            startt = device_dictionary[iter_device][2]
            # end time for dev
            endt = device_dictionary[iter_device][3]
            # thresholf for brightness to enable dev
            min_lux = device_dictionary[iter_device][4]
            # chance to switch dev on
            perc_on = device_dictionary[iter_device][5]
            # chance to switch dev off
            perc_off = device_dictionary[iter_device][6]
            new_dev = device(name, an, aus, startt, endt, min_lux, perc_on, perc_off)
            self.dev_class_list.append(new_dev)
        self.length = len(self.dev_class_list)
        self._delay = delay / self.length

    def set_latches(self, latch_on_dict, latch_off_dict):
        for iter_device in latch_on_dict:
            for iter_dev in self.dev_class_list:
                if iter_dev.name == iter_device:
                    iter_dev.latch_on = latch_on_dict[iter_device]
        for iter_device in latch_off_dict:
            for iter_dev in self.dev_class_list:
                if iter_dev.name == iter_device:
                    iter_dev.latch_off = latch_off_dict[iter_device]  
                    
    def set_increments(self, inc_list):
        for iter_device in inc_list:
            for iter_dev in self.dev_class_list:
                if iter_dev.name == iter_device:
                    iter_dev.incrememt = True
            
        
    def start(self):
        self.running = True
        toolbox.log('Ghost started', level=1)
        self.run()
        
    def run(self):
        while self.running:
            for iter_dev in self.dev_class_list:
                iter_dev.switch()
                time.sleep(self._delay)
                if not self.running:
                    break

    def stop(self):
        self.running = False
        toolbox.log('Ghost stopped', level=1)
                
dev_list = {'V00ESS1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                               datetime.time(22, 30, 0, 0), 60, 20, 50),
            'V00KUE1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                               datetime.time(22, 30, 0, 0), 60, 1, 10),
            'V00KUE1DEK1LI02':('On', 'Off', datetime.time(7, 0, 0, 0), 
                               datetime.time(22, 30, 0, 0), 60, 1, 10),
            'V00FLU1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                               datetime.time(22, 30, 0, 0), 60, 1, 15),
            'V01FLU1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                               datetime.time(22, 30, 0, 0), 60, 1, 15),
            'V00WOH1RUM1LI13':('Ambience', 'Aus', datetime.time(7, 0, 0, 0), 
                               datetime.time(23, 0, 0, 0), 60, 50, 25)}
min_off_dict = {'V00ESS1DEK1LI01':10,
                'V00KUE1DEK1LI01':5,
                'V00KUE1DEK1LI02':5,
                'V00FLU1DEK1LI01':30,
                'V01FLU1DEK1LI01':20,
                'V00WOH1RUM1LI13':3}
min_on_dict = {'V00ESS1DEK1LI01':10,
               'V00KUE1DEK1LI01':1,
               'V00KUE1DEK1LI02':1,
               'V00FLU1DEK1LI01':0,
               'V01FLU1DEK1LI01':0,
               'V00WOH1RUM1LI13':20}
increments = ['V00KUE1DEK1LI01',
              'V00KUE1DEK1LI02',
              'V00FLU1DEK1LI01',
              'V01FLU1DEK1LI01']
            
if __name__ == '__main__':
    ghost = anwesenheits_geist(dev_list)
    ghost.set_latches(min_off_dict, min_on_dict)
    ghost.set_increments(increments)
    ghost.start()