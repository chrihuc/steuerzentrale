# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:42:46 2017

@author: 212505558
"""

import unittest
import constants
import time

from inputs import cron


class TestUM(unittest.TestCase):

    def setUp(self):
        pass
#        self.crn = AES()

    def test_cron(self):
        constants.debug_text = 'cron'
        cron.periodic_supervision()
        time.sleep(120)
        constants.run = False

if __name__ == '__main__':
    unittest.main()