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

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

class AlarmListe:

    liste = {}

    def __init__(self):
        self.load()
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)


    def addAlarm(self, titel, text):
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        hash_id = str(uuid.uuid4())
        newAlarm = {'Titel':titel, 'Text':text, 'ts':uhr, 'uuid':hash_id}
        AlarmListe.liste[hash_id] = newAlarm
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)
        self.store()

    def delAlarm(self, uuid):
#        print(AlarmListe.liste)
        try:
            del AlarmListe.liste[uuid]
        except:
            print('error deleting alarm ', uuid)
        mqtt_pub("Message/Alarmliste", AlarmListe.liste)
        self.store()

    def store(self):
        with open('alarmlist.jsn', 'w') as fout:
            json.dump(AlarmListe.liste, fout, default=json_serial)

    def load(self):
        try:
            with open('alarmlist.jsn') as f:
                full = f.read()            
            AlarmListe.liste = json.loads(full)
        except:
            pass
#            toolbox.log('Laden der Szenen fehlgeschlagen', level=1)
        
class AES:

    alarm_liste = AlarmListe()        
        
def mqtt_pub(channel, data):
#    return
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))    
    if isinstance(data, dict):
        data['ts'] = uhr
#        print(data)
        data = json.dumps(data, default=handler, allow_nan=False)
#        print(data)
#        client.publish(channel, data, qos=1, retain=True)
    else:
        raise TypeError('Data is not a dictionary')        
        
        
aes = AES()
aeg = AES()
aes.alarm_liste.addAlarm('alarm1','ALARM1')
print(aeg.alarm_liste.liste)