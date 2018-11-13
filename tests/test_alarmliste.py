# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:26:19 2018

@author: hc
"""

import time, datetime
from time import  localtime, strftime
import uuid
import json

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds    
    else:
        return 'non Json'


class AlarmListe:

    liste = {}

    def __init__(self):
        pass
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)


    def addAlarm(self, titel, text):
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        hash_id = str(uuid.uuid4())
        newAlarm = {'Titel':titel, 'Text':text, 'ts':uhr, 'uuid':hash_id}
        AlarmListe.liste[hash_id] = newAlarm
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)

    def delAlarm(self, uuid):
        del AlarmListe.liste[uuid]
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)
        
        
def mqtt_pub(channel, data):
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
    if isinstance(data, dict):
        data['ts'] = uhr
        print(data)
        data = json.dumps(data, default=handler, allow_nan=False)
        print(data)
#        client.publish(channel, data, qos=1, retain=True)
    else:
        raise TypeError('Data is not a dictionary')        
        
        
ael = AlarmListe()
ael.addAlarm('alarm1','ALARM1')
