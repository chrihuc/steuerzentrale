# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:11:37 2017

@author: Christoph Huckle
"""

import unittest
from outputs import sonos
import time

class TestUM(unittest.TestCase):

    def setUp(self):
        self.test_mod = sonos.Sonos()

    def test_list_devices(self):
        list_devices = self.test_mod.list_devices()
        print(list_devices)
        print(list_devices)
        self.assertTrue(list_devices,
                         'Error getting devices')
#
#    def test_list_commands(self):
#        list_commands = self.test_mod.list_commands()
#        print(list_commands)
#        self.assertTrue(list_commands,
#                         'Error getting commands')
#
#    def test_dict_commands(self):
#        list_commands = self.test_mod.dict_commands()
#        print(list_commands)
#        self.assertTrue(list_commands,
#                         'Error getting commands')

    def test_klingel(self):
        result = self.test_mod.set_device('Kueche', 'Ansage', 'klingel.wav')
        self.assertTrue(result,
                         'Error sending command')
#
    def test_set_device(self):
#        result = self.test_mod.set_device('Bad', 'DRS3')
#        self.assertTrue(result,
#                         'Error sending command')
#        time.sleep(5)
        result = self.test_mod.set_device('Kueche', 'VolKuecheLeise')
        self.assertTrue(result,
                         'Error sending command')
#
#    def test_all_commands(self):
#        list_commands = self.test_mod.list_commands()
#        for command in list_commands:
#            self.test_mod.set_device('Kinderzimmer', command)
#        self.test_mod.set_device('Kinderzimmer', 'Pause')

#    def test_set_device(self):
#        self.test_mod.set_device('Kinderzimmer', 'unittest')

if __name__ == '__main__':
    unittest.main()