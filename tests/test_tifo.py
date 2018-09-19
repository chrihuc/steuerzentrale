#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 23:58:41 2017

@author: christoph
"""

import unittest
import time
import constants
from tifo import tf_connection
from tools import toolbox


class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
        constants.debug_level = 10
#        constants.debug_text = 'tf_conn'


#    def test_connect_1_conns(self):
#        self.test_mod = tf_connection.TiFo('localhost')


    def test_connect_2_conns(self):
        toolbox.log('test')
        #self.test_mod = tf_connection.TiFo('localhost')
#        toolbox.communication.register_callback(self.test_mod.receive_communication)
        self.test_mod2 = tf_connection.TiFo('192.168.193.102')
        self.test_mod2.main()
#        toolbox.communication.register_callback(self.test_mod2.receive_communication)


if __name__ == '__main__':
    unittest.main()