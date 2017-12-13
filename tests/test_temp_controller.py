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
        pass
#        constants.debug = True

#    def test_get_zones(self):
#        TempController.get_zones()
#        print TempController.zones
#        
#    def test_init_rooms(self):
#        TempController.init_rooms()
#        print TempController.rooms        
#
#    def test_update_setpoints(self):
#        TempController.update_setpoints()
#
    def test_whole_module(self):
        TempController.start()
        time.sleep(60)
        TempController.stop()
#
#    def test_stop(self):
#        TempController.stop()

#        self.assertTrue(True,
#                         'Failed to Execute Scene')   

if __name__ == '__main__':
    unittest.main()