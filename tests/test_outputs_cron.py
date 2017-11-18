# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 19:52:27 2016

@author: Christoph Huckle
"""

import unittest
from outputs import cron

class TestUM(unittest.TestCase):

    def setUp(self):
        self.crn = cron.Cron()

#    def test_inputs(self):
#        print self.crn.get_all(typ='Gui')
##        self.assertFalse(mysql_connector.inputs('V01KID1RUM1TE01', 23),
##                         'Inputs function returning wrong scenes')

#    def test_calculate(self):
#        result = self.crn.calculate()
#        self.assertTrue(result,
#                         'Recalculation of crontable not working')

    def test_get_now(self):
    #crn.new_event('Test','20:15')
       print self.crn.get_now(2, '19:29')
#    print crn.get_all()
#    crn.executed(14)


if __name__ == '__main__':
    unittest.main()