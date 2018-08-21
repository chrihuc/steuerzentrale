#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

import paho.mqtt.client as mqtt  #import the client1
import time
import json
import constants

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
        client.subscribe("Inputs/ESP/#")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))    
    try:
        m_in=(json.loads(msg.payload)) #decode json data
        print m_in
        if 'Value' in m_in:
            name = msg.topic[7:]
            print 'Name: ', name            
            #print 'Value: ', float(m_in['Value'])
    except ValueError:
        print("no json code")

    
mqtt.Client.connected_flag=False#create flag in class
broker=constants.mqtt_.server
client = mqtt.Client(constants.name)
client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
client.connect(constants.mqtt_.server)           #create new instance 
client.on_connect=on_connect  #bind call back function
client.on_message = on_message
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker)      #connect to broker
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
print("in Main Loop")

try:
    while True:
        pass
except KeyboardInterrupt:
    pass
client.loop_stop()    #Stop loop 
client.disconnect() # disconnect