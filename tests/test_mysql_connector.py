# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:11:37 2017

@author: Christoph Huckle
"""

import unittest
from database import mysql_connector

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_inputs(self):
        self.assertFalse(mysql_connector.inputs('V01KID1RUM1TE01', 23),
                         'Inputs function returning wrong scenes')
    
    def test_get_device_adress(self):
        print mysql_connector.get_device_adress('Vm1ZIM1SAT1LI01')
    
if __name__ == '__main__':
    unittest.main()