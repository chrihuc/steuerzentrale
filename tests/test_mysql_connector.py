# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:11:37 2017

@author: Christoph Huckle
"""

import unittest
from database import mysql_connector
import numpy as np
import time

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_inputs(self):
        self.assertTrue(mysql_connector.inputs('V01KID1RUM1TE01', 23),
                         'Inputs function returning wrong scenes')
    
    def test_get_device_adress(self):
        print mysql_connector.get_device_adress('Vm1ZIM1SAT1LI01')
    
    def test_tables_no_init(self):
#        scenes_df = mysql_connector.tables.scenes_df
#        print scenes_df.loc[scenes_df['Name'] == 'Adress']
#        aktors_df = mysql_connector.tables.aktors_df
#        types = aktors_df[aktors_df.index == 'Device_Type'].values[0]
#        types = [x for x in types if not x in [np.nan, None]]
#        print mysql_connector.tables.akt_type_dict
#        print aktors_df[aktors_df.index == 'Adress'].to_dict(orient='records')[0]
        print mysql_connector.tables().inputs_dict['XS1.V01BAD1RUM1TE01']['last1']
#        print scenes_df.set_index('Name').to_dict()

    def test_tables_reload(self):
        print mysql_connector.tables.inputs_dict['XS1.V01BAD1RUM1TE01']['last1']
        time.sleep(60)
        mysql_connector.tables.reload_inputs()
        print mysql_connector.tables.inputs_dict['XS1.V01BAD1RUM1TE01']['last1']        

#    def test_debounce(self):
#        print mysql_connector.inputs('Test', 0)
#        print mysql_connector.inputs('Test', 0)
#        self.assertTrue(mysql_connector.inputs('Test', 23),
#                         'Inputs function returning wrong scenes')        

#    def test_tables_reload(self):
#        mysql_connector.tables.reload_scenes()
#        print mysql_connector.tables.scenes_df.columns
    
if __name__ == '__main__':
    unittest.main()