#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 13:24:22 2017

@author: christoph
"""

import unittest

import constants
from outputs.szenen import Szenen
from tools import toolbox
import time, datetime

from tifo import tf_connection

class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
#        self.tifo = tf_connection.TiFo()
        self.sz = Szenen()
        self.start_t = None

    def print_it(self, it):
        print datetime.datetime.now() - self.start_t, it


#
#    def test_WohnziAnw0(self):
#        runs = self.sz.execute("WohnziAnw1")
#        self.assertTrue(runs,
#                         'Failed to Execute Scene')
        
#    def test_test(self):
#        runs = self.sz.execute("Test")
#        self.assertTrue(runs,
#                         'Failed to Execute Scene')        
#
#    def test_send_message(self):
#        payload = {'Device':'V00WOH1RUM1ST01','Command':'22'}
#        toolbox.communication.send_message(payload, typ='SetDevice')
#        toolbox.communication.send_message(payload)


#    def test_heartbeat_input(self):
#        payload = {'Name':'XS1.V01SCH1RUM1TE01','Value':'20.51'}
#        toolbox.communication.send_message(payload)
#        time.sleep(20)
#        toolbox.communication.send_message(payload)

    def test_execute0(self):
        runs = self.sz.execute("HeizungTag")
        self.assertTrue(runs,
                         'Failed to Execute Scene')
    
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