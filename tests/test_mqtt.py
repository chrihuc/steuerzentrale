#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:46:03 2018

@author: christoph
"""
#import paho.mqtt.client as mqtt
#
#import constants
#from tools import toolbox
#import json
from outputs.mqtt_publish import mqtt_pub

#client = mqtt.Client(constants.name)
#client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
#client.connect(constants.mqtt_.server)
#client.connect('127.0.0.1')

key = "test"
wert = '1'
dicti = {'Key':key, 'Value':wert}
#data = json.dumps('{Value:%s, Key:%s}' % (wert, key), default=toolbox.handler, allow_nan=False)
#data = json.dumps(dicti, default=toolbox.handler, allow_nan=False)
#print data
#data = '{"Value":"%s", "Key":"%s"}' % (wert, key)
#client.publish("Inputs/" + key, data, qos=1)
mqtt_pub("Command/Szene/AlarmanlageEin", dicti)