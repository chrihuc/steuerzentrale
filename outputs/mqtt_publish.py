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
import os, sys, re
from time import localtime,strftime
from tools import toolbox

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

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
        uhr = str(strftime("%Y-%m-%d_%H_%M_%S",localtime(zeit)))
        self.client = mqtt.Client(client_id=constants.name +'_pub_' + uhr, clean_session=False)
        self.client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
        self.ip = ip
        toolbox.communication.register_callback(self.receive_communication)
        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+ str(rc))
        self.connected = True
#        client.subscribe("test")

    def connect(self):
        self.client.connect(self.ip, 1883, 60)
        print("connecting")
        self.client.on_connect = self.on_connect
        self.client.loop_start()
    
    
    def mqtt_pub(self, channel, data, retain=True, short=False):
        if not self.connected:
            time.sleep(5)
            if not self.connected: self.connect()
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
        if isinstance(data, dict):
            if not short:
                data['ts'] = uhr
            try:
                if 'Value' in data:
                    try:
                        data['Value'] = round(float(data['Value']), 2)
                    except:
                        pass
                data = json.dumps(data, default=handler, allow_nan=False)
            except:
                self.client.publish(channel, "couldn't convert to json", qos=1, retain=True)
            else:
                self.client.publish(channel, data, qos=1, retain=retain)
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
        return True

    def receive_communication(self, payload, *args, **kwargs):
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and (toolbox.kw_unpack(kwargs,'receiver') in ['MQTT', 'ESP']):
            adress=toolbox.kw_unpack(kwargs,'adress')
            device = adress.split(".")[1] 
#            der teil muss abgekürzt werden, wenn ein ESP der empfänger ist, auf nur das nötigste
            if toolbox.kw_unpack(kwargs,'receiver') == 'ESP':
                new_pl = {}
                new_pl['Value'] = payload['Value']
                new_pl['SleepTime'] = payload['SleepTime']
                result = self.mqtt_pub("Outputs/" + device, new_pl, short=True)
                toolbox.communication.send_message(payload, typ='return', value=result)
#                 mosquitto_pub -h 192.168.192.2 -t shellies/shelly1-B91B5A/relay/0/command  -m "off" -u customer -P 'wR,*BnoQ7i0fy\6hj6F'
#            elif toolbox.kw_unpack(kwargs,'receiver') == 'Shelly':
#                result = self.mqtt_pub("shellies/" + device + adress.split(".")[2], payload['Value'])
#                toolbox.communication.send_message(payload, typ='return', value=result)                
            else:
                payload['adress'] = toolbox.kw_unpack(kwargs,'adress')
                result = self.mqtt_pub("Command/" + device, payload)
                toolbox.communication.send_message(payload, typ='return', value=result)

def ping(IP, number = 1):
    pinged = False
    if IP == None:
        return False
    else:
        lifeline = re.compile(r"(\d) received")
        for i in range(0,number):
            pingaling = os.popen("ping -q -c 2 "+IP,"r")
            sys.stdout.flush()
            while 1==1:
               line = pingaling.readline()
               if not line: break
               igot = re.findall(lifeline,line)
               if igot:
                if int(igot[0])==2:
                    pinged = True
                else:
                    pass
        return pinged

for mqtt_con in constants.mqtt_.server: 
    if ping(mqtt_con):             
        mq_cli = MqttClient(mqtt_con)
        mqtt_list.append(mq_cli)
        
if not mqtt_list:
    print("Kein MQTT Server gefunden")        

def mqtt_pub(channel, data, retain=True):
    for cli in mqtt_list:
#        print(cli.ip)
#        print(channel, data, retain)
        cli.mqtt_pub(channel, data, retain)
           