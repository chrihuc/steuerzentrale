#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 13:24:22 2017

@author: christoph
"""

import unittest
from outputs.szenen import Szenen

class TestUM(unittest.TestCase):

    def setUp(self):
        self.sz = Szenen()

    def test_Ambience(self):
        runs = self.sz.execute("Ambience")
        self.assertTrue(runs,
                         'Failed to Execute Scene')

#    def test_pause(self):
#        runs = self.sn.set_device('V01KID1RUM1AV11','Pause')
#        self.assertTrue(runs,
#                         'Failed to pause')
#        
if __name__ == '__main__':
    unittest.main()