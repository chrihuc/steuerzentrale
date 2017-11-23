#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:10:49 2017

@author: christoph
"""


import unittest
import constants
from database import kivy_mysql_connector as kmc

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

#    def test_get_table(self):
#        print kmc.get_table(constants.sql_tables.szenen.name)

    def test_list_scenes(self):
        print kmc.list_scenes()
        print kmc.list_scenes('Wecker')
        print kmc.list_scenes(['Favorit', 'Gui'])
    
    
if __name__ == '__main__':
    unittest.main()