#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:46:03 2018

@author: christoph
"""
import paho.mqtt.client as mqtt

import constants
from tools import toolbox
import json

client = mqtt.Client(constants.name)
client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
client.connect(constants.mqtt_.server)

wert = 'test'
setting = 1
data = json.dumps('{"Value":"%s", "Key":"%s"}' % (wert, setting), default=toolbox.handler, allow_nan=False)
client.publish("Inputs/" + wert, data, qos=1)