# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:36:06 2019

@author: hc
"""

import constants

from secvest.secvest import Secvest


alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
alarmanlage.logout()
