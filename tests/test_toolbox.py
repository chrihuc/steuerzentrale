#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:57:22 2017

@author: christoph
"""

import unittest
from tools import toolbox
import constants

class TestUM(unittest.TestCase):

    def setUp(self):
#        pass
        toolbox.communication.register_callback(self.print_it)
        print(toolbox.communication.callbacks)

    def print_it(self, payload, *args, **kwargs):
        print('args:', args)
        print('kwargs:', kwargs)
        print('typ:', toolbox.kw_unpack(kwargs,'typ'))
        print('payload:', payload)
        
    def test_log(self):
        constants.debug = True
        constants.debug_level = 10        
        toolbox.log("test")
#
#    def test_ip(self):
#        print(toolbox.check_ext_ip())

#    def test_send_message(self):
#        payload = {'Device':'Device 1','Command':'An'}
#        toolbox.communication.send_message(payload, typ='SetDevice')
#        toolbox.communication.send_message(payload)

#    def test_sleep_1(self):
#        toolbox.sleep(10)


if __name__ == '__main__':
    unittest.main()