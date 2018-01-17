#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:52:01 2017

@author: christoph
"""

import unittest
from outputs import xs1

class TestUM(unittest.TestCase):

    def setUp(self):
        self.test_mod = xs1.XS1()

#    def test_list_devices(self):
#        list_devices = self.test_mod.list_devices()
#        print list_devices
#        self.assertTrue(list_devices,
#                         'Error getting devices')
#
#    def test_list_commands(self):
#        list_commands = self.test_mod.list_commands()
#        print list_commands
#        self.assertTrue(list_commands,
#                         'Error getting commands')
#    
#    def test_set_device(self):
#        result = self.test_mod.set_device('Adventslichter1', 'An')
#        self.assertTrue(result,
#                         'Error sending command')  

    def test_set_device_fht(self):
        result = self.test_mod.set_device('V00KUE1RUM1ST01', 21.3)
        self.assertTrue(result,
                         'Error sending command')    
    
#    def test_list_raw_senors(self):
#        print self.test_mod.list_sensors()
 
#    def test_list_raw_senors(self):
#        print self.test_mod.list_actors()
       
#    def test_check_batteries(self):
#        self.test_mod.check_batteries()
        
#    def test_all_commands(self):
#        list_commands = self.test_mod.list_commands()
#        list_devices = self.test_mod.list_devices()
#        for device in list_devices:
#            for command in list_commands:
#                self.test_mod.set_device(device, command)


if __name__ == '__main__':
    unittest.main()