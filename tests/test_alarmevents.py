#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 16:31:33 2017

@author: christoph
"""

import unittest
from alarm_event_messaging.alarmevents import AES

class TestUM(unittest.TestCase):

    def setUp(self):
        self.aes = AES()

    def test_laod_evetns(self):
        runs = self.aes.alarm_events_read(unacknowledged=True, prio=1)
        self.assertTrue(runs,
                         'Failed to get events')

    def test_sendmail(self):
        result = self.aes.send_mail('test', 'TEST')
        
if __name__ == '__main__':
    unittest.main()