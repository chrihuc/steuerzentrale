#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christoph
"""


import unittest
from outputs import tradfri

class TestUM(unittest.TestCase):

    def setUp(self):
        self.test_mod = tradfri.Tradfri_lights()

#    def test_list_devices(self):
#        list_devices = self.test_mod.list_devices()
#        print(list_devices)
#        self.assertTrue(list_devices,
#                         'Error getting devices')

    def test_list_commands(self):
        list_commands = self.test_mod.list_commands()
        print(list_commands)
        print(self.test_mod.devices)
        self.assertTrue(list_commands,
                         'Error getting commands')
#    
    def test_set_device(self):
        result = self.test_mod.set_device('StehlampeRGB', 'Nacht')
        self.assertTrue(result,
                         'Error sending command')  
# 
#    def test_all_commands(self):
#        list_commands = self.test_mod.list_commands()
#        list_devices = self.test_mod.list_devices()
#        for device in list_devices:
#            for command in list_commands:
#                self.test_mod.set_device(device, command)


if __name__ == '__main__':
    unittest.main()