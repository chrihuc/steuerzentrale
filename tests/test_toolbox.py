#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:57:22 2017

@author: christoph
"""

import unittest
from tools import toolbox

class TestUM(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_ip(self):
        print toolbox.check_ext_ip()
        

if __name__ == '__main__':
    unittest.main()