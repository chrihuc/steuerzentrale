#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 05:07:08 2020

@author: christoph
"""

import unittest
from inputs import homematic

class TestUM(unittest.TestCase):

    def setUp(self):
#        pass
        homematic.main()

#    def print_it(self, payload, *args, **kwargs):
#        print('args:', args)

    def test_ip(self):
        print("testing")

if __name__ == '__main__':
    unittest.main()