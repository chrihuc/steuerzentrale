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
import uuid

#def callback_receiver(payload, *args, **kwargs):
#    print(payload, args, kwargs)
#
#toolbox.communication.register_callback(callback_receiver)

class TestUM(unittest.TestCase):

    def setUp(self):
        constants.debug = True
        constants.debug_level = 0
        self.test_mod2 = tf_connection.TiFo('192.168.192.2')
        self.test_mod2.main()

#        constants.debug_text = 'tf_conn'


#    def test_connect_1_conns(self):
#        data = {'Name': 'Hell', 'red_1': None, 'red_2': '0', 'transitiontime': None, 'green_2': '0', 'green_1': None, 'Szene': 'Hell', 'blue': '255', 'Szene_id': uuid.uuid4(), 'transition': None, 'blue_2': '0', 'blue_1': None, 'green': '255', 'Device': 'V00WOH1SRA1LI01', 'percentage': None, 'Id': 1L, 'red': '255'}
#        self.test_mod2.set_device(data)
#        self.test_mod = tf_connection.TiFo('localhost')


    def test_connect_2_conns(self):
        toolbox.log('test')
#        self.test_mod2.main()


if __name__ == '__main__':
    unittest.main()