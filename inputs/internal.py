#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:03:49 2017

@author: christoph
"""

import time
import constants
from tools import toolbox as tb
from database import mysql_connector as msqc

from tools import toolbox
#toolbox.log('debug on')

# TODO: unittest


class Anwesenheit:
    def __init__(self):
        self.data = []


    def check_handys(self):
        toolbox.log()
        bewohner = msqc.mdb_get_table(constants.sql_tables.Bewohner.name)
        for person in bewohner:
            ip_adress = person['Handy_IP']
            if ip_adress == None:
                continue
            state = person['Handy_State']
            if state == None:
                state = 0
            else:
                state = int(state)
            if tb.ping(ip_adress):
                person['Handy_State'] = 5
            else:
                person['Handy_State'] = state - 1
            cmd = {'Handy_State':person['Handy_State']}
            msqc.mdb_set_table(constants.sql_tables.Bewohner.name, person['Name'], cmd)

    def check_handys_service(self):
        while True:
            self.check_handys()
            time.sleep(60)

if __name__ == "__main__":
    anw_class = Anwesenheit()
    anw_class.check_handys()
