#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 07:02:57 2019

@author: christoph
"""

from outputs.mqtt_publish import mqtt_pub
import constants
import time

time.sleep(10)

command = {'Szene':'FalscherPin'}
mqtt_pub("Command/Szene/FalscherPin", command)                 
                