#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:08:14 2017

@author: christoph
"""

    
import random
import time, datetime
from mysql_con import setting_r

# TODO: class scene
# TODO: operationalize it, 
# TODO Tests split adress from hks

delay = 1 * 60

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
    
    def switch(self):
        now = datetime.datetime.now()
        if self.startt > now.time() or now.time() > self.endt:
            if self.status:
                self.set_device(self.perc_off)
                self.last_switch = now
                return                
                
        lux = setting_r('V00WOH1RUM1HE01')
        if self.min_lux > 0 and self.min_lux > lux:
            return
                            
        if self.status:
            commando = self.aus
            wahrscheinlichkeit = self.perc_off
        else:
            commando = self.an
            wahrscheinlichkeit = self.perc_on       

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
            print now, self.name, commando
            self.set_device(commando)
            self.last_switch = now
        
    def set_device(self, commando):
#        set_szenen.set_device(self.name, commando)
        self.status = not self.status
        
class anwesenheits_geist(object):
    
    def __init__(self, device_dictionary):
        self.dev_class_list = []
        self.running = False
        for iter_device in device_dictionary:
            name = iter_device
            an = device_dictionary[iter_device][0]
            aus = device_dictionary[iter_device][1]
            startt = device_dictionary[iter_device][2]
            endt = device_dictionary[iter_device][3]
            min_lux = device_dictionary[iter_device][4]
            perc_on = device_dictionary[iter_device][5]
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
        
    def start(self):
        self.running = True
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
                
dev_list = {'V00WOH1RUM1LI01':('On', 'Off', datetime.time(12, 0, 0, 0), datetime.time(22, 0, 0, 0), 0, 10, 50)}
min_off_dict = {'V00WOH1RUM1LI01':10}
min_on_dict = {'V00WOH1RUM1LI01':3}
            
if __name__ == '__main__':
    ghost = anwesenheits_geist(dev_list)
    ghost.set_latches(min_off_dict, min_on_dict)
    ghost.start()