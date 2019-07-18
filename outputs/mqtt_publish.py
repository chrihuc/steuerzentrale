#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

import constants
import paho.mqtt.client as mqtt
import json
import datetime
import time
from time import localtime,strftime

mqtt_list = []

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # if entry is timedelta then use seconds as the value unit
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds
    else:
        return 'non Json'

class MqttClient():
    def __init__(self, ip):
        self.connected = False
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        self.client = mqtt.Client(constants.name +'_pub_' + uhr)
        self.client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
        self.ip = ip

    def connect(self):
        self.client.connect(self.ip)
        self.connected = True
        self.client.loop_start()
    
    
    def mqtt_pub(self, channel, data, retain=True):
        if not self.connected:
            self.connect()
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
        if isinstance(data, dict):
            data['ts'] = uhr
            try:
                data = json.dumps(data, default=handler, allow_nan=False)
            except:
                self.client.publish(channel, "couldn't convert to json", qos=1, retain=True)
            else:
                self.client.publish(channel, data, qos=1, retain=retain)
                print(channel)
        elif isinstance(data, list):
            data = {'payload': data, 'ts': uhr}
            try:
                data = json.dumps(data, default=handler, allow_nan=False)
            except:
                self.client.publish(channel, "couldn't convert to json", qos=1, retain=True)
            else:
                self.client.publish(channel, data, qos=1, retain=retain)            
        else:
            self.client.publish(channel, data, qos=1, retain=retain)

for mqtt_con in constants.mqtt_.server:            
    mq_cli = MqttClient(mqtt_con)
    mqtt_list.append(mq_cli)

def mqtt_pub(channel, data, retain=True):
    for cli in mqtt_list:
#        print(cli.ip)
#        print(channel, data, retain)
        cli.mqtt_pub(channel, data, retain)
           