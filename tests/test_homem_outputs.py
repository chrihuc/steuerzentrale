#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:39:58 2020

@author: christoph
"""

import unittest
from outputs import homematic
from tools import toolbox
import time

class TestUM(unittest.TestCase):

    def setUp(self):
        t = toolbox.OwnTimer(0, function=homematic.main, args = [], name="homematic")
        t.start()
#        time.sleep(10)
#        print(toolbox.communication.callbacks)

    def test_send_message(self):
        time.sleep(10)
        payload = {'Device': 'device', 'Szene': 'commando', 'Szene_id': 'szn_id', 'Value':20}
        toolbox.communication.send_message(payload, typ='output', receiver='CCU', adress='CCU.ip.001198A99FB4CD.set_temperature')
#        print("done")

if __name__ == '__main__':
    unittest.main()