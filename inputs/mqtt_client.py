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

def connect(ipaddress, port):
    global client
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    client = mqtt.Client(constants.name +'_sub_' + uhr, clean_session=False)
    assign_handlers(on_connect, dis_con, on_message)
    client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
    client.connect(ipaddress, port, 60)
#    client.loop_start()
    client.loop_forever()


def assign_handlers(connect, disconnect, message):
    """
    :param mqtt.Client client:
    :param connect:
    :param message:
    :return:
    """

    global client
    client.on_connect = connect
    client.on_disconnect = disconnect
    client.on_message = message


def on_connect(client_data, userdata, flags, rc):
    global client, topics
    if rc==0 and not client.connected_flag:
        client.connected_flag=True #set flag
        print("connected OK")
        for topic in topics:
            client.subscribe(topic)
    elif client.connected_flag:
        pass
    else:
        print("Bad connection Returned code=",rc)
#    print "connected"
#    client.subscribe(topic)

def dis_con (*args, **kargs):
    print("disconnected")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    message = str(msg.payload.decode("utf-8"))
    retained = message.retain
    try:
        m_in=(json.loads(message)) #decode json data
        print(m_in)
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
                if 'uuid' in m_in.keys:
                    print(m_in['uuid'])
                    aes.alarm_liste.delAlarm(m_in['uuid'])
        if 'DataRequest' in msg.topic:
            if 'Wecker' in msg.topic:
                print('DataRequest Wecker')
                mqtt_pub("DataRequest/Answer/Wecker", crn.get_all(wecker=True))
    except ValueError:
        pass
        print("no json code", message)

mqtt.Client.connected_flag=False
client = None
topics = ["Inputs/ESP/#", "Command/#", "Message/AlarmOk", "Inputs/Satellite/#", "DataRequest/Request/#"]
ipaddress = constants.mqtt_.server
port = 1883



def main():
    global client, topic, ipaddress, port
    connect(ipaddress, port)


if __name__ == "__main__":
    topics = ["Inputs/#"]
    ipaddress = '127.0.0.1'
    main()