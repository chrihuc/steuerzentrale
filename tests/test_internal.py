#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:11:30 2017

@author: christoph
"""

import unittest
from outputs import internal

class TestUM(unittest.TestCase):

    def setUp(self):
        self.test_mod = internal.Internal()

    def test_list_devices(self):
        anwesenheit = self.test_mod.check_anwesenheit()
        self.assertTrue(anwesenheit,
                         'Error checking Anwesenheit')



if __name__ == '__main__':
    unittest.main()
