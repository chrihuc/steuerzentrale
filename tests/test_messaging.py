#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:24:26 2017

@author: christoph
"""

import unittest
from alarm_event_messaging.messaging import Messaging

class TestUM(unittest.TestCase):

    def setUp(self):
        self.test_mod = Messaging()

    def test_send_direkt(self):
        result = self.test_mod.send_direkt(to="Christoph", titel="Test", text="Test")
        self.assertTrue(result,
                         'Failed to get events')

        
if __name__ == '__main__':
    unittest.main()