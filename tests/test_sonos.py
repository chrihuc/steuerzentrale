# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:11:37 2017

@author: Christoph Huckle
"""

import unittest
from outputs.sonos import Sonos

class TestUM(unittest.TestCase):

    def setUp(self):
        self.sn = Sonos()

    def test_play(self):
        runs = self.sn.set_device('V01KID1RUM1AV11','Play')
        self.assertTrue(runs,
                         'Failed to play')

    def test_pause(self):
        runs = self.sn.set_device('V01KID1RUM1AV11','Pause')
        self.assertTrue(runs,
                         'Failed to pause')
        
if __name__ == '__main__':
    unittest.main()