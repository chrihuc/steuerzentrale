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

connected = False

zeit =  time.time()
uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
client = mqtt.Client(constants.name +'_pub_' + uhr)
client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)

def connect():
    global connected
    client.connect(constants.mqtt_.server)
    connected = True
    client.loop_start()

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # if entry is timedelta then use seconds as the value unit
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds
    else:
        return 'non Json'

def mqtt_pub(channel, data, retain=True):
    if not connected:
        connect()
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
    if isinstance(data, dict):
        data['ts'] = uhr
        try:
            data = json.dumps(data, default=handler, allow_nan=False)
        except:
            client.publish(channel, "couldn't convert to json", qos=1, retain=True)
        else:
            client.publish(channel, data, qos=1, retain=retain)
    else:
        client.publish(channel, data, qos=1, retain=retain)