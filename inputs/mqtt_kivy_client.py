# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:29:37 2019

@author: hc
"""

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

class MqttClient:
    def __init__(self, ip, topics, on_mes):
        self.port = 1883
        self.ip = ip
        self.topics = topics
        self.client = None
        self.status = None
        self.on_mes = None
        

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
            if 'Settings' in msg.topic:             
                if 'Status' in msg.topic:  
                    self.status = m_in['Value']
            if self.on_mes:
                self.on_mes(msg.topic, m_in) 
                

mqtt.Client.connected_flag=False
#client = None
             


if __name__ == "__main__":
    topics = ["Inputs/#"]
    constants.mqtt_.server = ['127.0.0.1']
