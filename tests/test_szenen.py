#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 13:24:22 2017

@author: christoph
"""

import unittest

import constants
from outputs.szenen import Szenen
import time, datetime

class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
        self.sz = Szenen()
        self.start_t = None

    def print_it(self, it):
        print datetime.datetime.now() - self.start_t, it


#
#    def test_WohnziAnw0(self):
#        runs = self.sz.execute("WohnziAnw1")
#        self.assertTrue(runs,
#                         'Failed to Execute Scene')
        
    def test_test(self):
        runs = self.sz.execute("Test")
        self.assertTrue(runs,
                         'Failed to Execute Scene')        

#    def test_execute0(self):
#        runs = self.sz.execute("RestartSatellites")
#        self.assertTrue(runs,
#                         'Failed to Execute Scene')
    
#    def test_timer_add(self):
#        self.start_t = datetime.datetime.now()
#        self.sz.timer_add(self.print_it, parent = "Bad_ir",delay = 10, child = "Bad_aus", exact = False, retrig = True)
#        Szenen.sz_t.zeige()
#        time.sleep(8)
#        Szenen.sz_t.zeige()
#        time.sleep(5)
#        Szenen.sz_t.zeige()

if __name__ == '__main__':
    unittest.main()