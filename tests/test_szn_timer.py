#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:17:30 2017

@author: christoph
"""

import time
import datetime
import unittest

import constants
from tools import szn_timer

class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
        self.test_mod = szn_timer.Szenen_Timer(callback=self.print_it)
        self.start_t = None

    def print_it(self, it, device):
        print datetime.datetime.now() - self.start_t, it

    def test_list_devices(self):
        self.start_t = datetime.datetime.now()
        print self.test_mod.retrigger_add(parent = "Bad_ir",delay = 10, child = "Bad_aus", exact = False, retrig = True)
        time.sleep(5)
        self.test_mod.zeige()
#        self.assertTrue(list_devices,
#                         'Error getting devices')


if __name__ == '__main__':
    unittest.main()