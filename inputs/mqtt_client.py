#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

import paho.mqtt.client as mqtt
import json
import constants
import time
from time import localtime,strftime
from tools import toolbox

from alarm_event_messaging import alarmevents
from database import mysql_connector as msqc
from outputs import cron
from outputs.mqtt_publish import mqtt_pub
aes = alarmevents.AES()
crn = cron.Cron()

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value)
    toolbox.communication.send_message(payload, typ='InputValue')

def broadcast_exec_szn(szene):
    payload = {'Szene':szene}
#    on server:
    toolbox.communication.send_message(payload, typ='ExecSzene')

def broadcast_exec_comm(device, command):
    payload = {'Device':device, 'Command':command}
#    on server:
    toolbox.communication.send_message(payload, typ='SetDevice')

class MqttClient:
    def __init__(self, ip, topics):
        self.port = 1883
        self.ip = ip
        self.topics = topics
        self.client = None
        

    def connect(self):
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        self.client = mqtt.Client(constants.name +'_sub_' + uhr, clean_session=False)
        self.assign_handlers(self.on_connect, self.dis_con, self.on_message)
        self.client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
        self.client.connect(self.ip, self.port, 60)
    #    client.loop_start()
        self.client.loop_forever()
    
    
    def assign_handlers(self, connect, disconnect, message):
        """
        :param mqtt.Client client:
        :param connect:
        :param message:
        :return:
        """

        self.client.on_connect = connect
        self.client.on_disconnect = disconnect
        self.client.on_message = message
    
    
    def on_connect(self, client_data, userdata, flags, rc):
        if rc==0 and not self.client.connected_flag:
            self.client.connected_flag=True #set flag
            print("connected OK")
            for topic in self.topics:
                self.client.subscribe(topic)
        elif self.client.connected_flag:
            pass
        else:
            print("Bad connection Returned code=",rc)
    #    print "connected"
    #    client.subscribe(topic)
    
    def dis_con (self, *args, **kargs):
        print("disconnected")
    
    def on_message(self, client, userdata, msg):
    #    print(msg.topic + " " + str(msg.payload))
        message = str(msg.payload.decode("utf-8"))
        retained = msg.retain
    #    print(retained)
        try:
            m_in=(json.loads(message)) #decode json data
        except ValueError:
            print("no json code", message)
        else:        
    #        print(m_in)
    #        print(msg.topic + " " + str(msg.payload))        
            if not retained:
                if 'Inputs' in msg.topic:
                    name = msg.topic[7:]
                    if 'Value' in m_in.keys():
                        broadcast_input_value('MQTT.' + name, float(m_in['Value']))
                elif 'Command' in msg.topic:
                    if 'Szene' in msg.topic:
                        szene = msg.topic.split('/')[2]
                        broadcast_exec_szn(szene)
                    if 'Device' in msg.topic:
                        device = m_in['Device']
                        command = m_in['Command']
                        broadcast_exec_comm(device, command)
                elif 'AlarmOk' in msg.topic:
                    if 'uuid' in m_in.keys():
                        aes.alarm_liste.delAlarm(m_in['uuid'])
                elif 'AlarmListClear' in msg.topic:
                    aes.alarm_liste.clear()                        
                elif 'SetWecker' in msg.topic:
                    table = constants.sql_tables.cron.name
                    for entry in eval(m_in['SetWecker']):
                        device = entry['Name']
                        msqc.mdb_set_table(table, device, entry) 
                elif 'SetSettings' in msg.topic:
                    table = constants.sql_tables.settings.name
                    msqc.setting_s(m_in['Name'], m_in['Value'])                    
            if 'DataRequest' in msg.topic:
                if 'SetTable' in msg.topic:  
                    table = constants.sql_tables.cron.name
                    for entry in m_in['payload']:
    #                    print(entry)
                        device = entry['Name']
                        msqc.mdb_set_table(table, device, entry)            
                elif 'Wecker' in m_in.values():
    #                print('DataRequest Wecker')
                    mqtt_pub("DataRequest/Answer/Cron", crn.get_all(wecker=True))
                elif 'Schaltuhr' in m_in.values():
                    mqtt_pub("DataRequest/Answer/Cron", crn.get_all(typ='Gui'))
                elif 'GetSettings' in m_in.values():
                    mqtt_pub("DataRequest/Answer/Settings", msqc.mdb_get_table(constants.sql_tables.settings.name)) 
                elif 'SzenenGruppen' in m_in.values():
                    mqtt_pub("DataRequest/Answer/SzenenGruppen", msqc.mdb_read_table_columns(constants.sql_tables.szenen.name, ['Name','Gruppe','Beschreibung']))
                

mqtt_list = []
mqtt.Client.connected_flag=False
#client = None
topics = ["Inputs/ESP/#", "Command/#", "Message/AlarmOk", "Inputs/Satellite/#", "DataRequest/Request/#", "DataRequest/SetTable/#", 
          "DataRequest/SetSettings/#", "Message/AlarmListClear"]


def main():
    for mqtt_con in constants.mqtt_.server:            
        mq_cli = MqttClient(mqtt_con, topics)
        mq_cli.connect()
        mqtt_list.append(mq_cli)    


if __name__ == "__main__":
    topics = ["Inputs/#"]
    constants.mqtt_.server = ['127.0.0.1']
    main()