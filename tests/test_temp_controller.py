#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:01:31 2017

@author: christoph
"""

import unittest


import time
import constants
from outputs.temp_control import TempController


class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
        constants.debug_level = 10
        pass
#        constants.debug = True

#    def test_load_zones(self):
#        TempController.load_zones()
#        print TempController.zones
#       
#    def test_get_temp(self):
#        TempController.load_zones()
#        print TempController.zones[0].get_act_temp()
#       
#    def test_get_set_value(self):
#        TempController.load_zones()
#        print TempController.zones[0].get_set_value()
#
#    def test_get_act_reading(self):
#        TempController.load_zones()
#        print TempController.zones[0].get_actuator_temp() 
#       
#    def test_cycle(self):
#        TempController.load_zones()
#        print TempController.zones[0].cycle() 
        
#    def test_update_setpoints(self):
#        TempController.update_setpoints()
#
    def test_whole_module(self):
        TempController.start_thread()
        time.sleep(120)
        TempController.stop()
#
#    def test_stop(self):
#        TempController.stop()

#    def test_read_sql(self):
#        TempController.read_sql()
#        self.assertTrue(True,
#                         'Failed to Execute Scene')   

if __name__ == '__main__':
    unittest.main()