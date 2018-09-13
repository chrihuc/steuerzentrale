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

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value)
    toolbox.communication.send_message(payload, typ='InputValue')


def connect(ipaddress, port):
    global client
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    client = mqtt.Client(constants.name +'_sz_' + uhr, clean_session=False)
    assign_handlers(on_connect, dis_con, on_message)
    client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
    client.connect(ipaddress, port, 60)
    client.loop_start()
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
    global client, topic
    if rc==0 and not client.connected_flag:
        client.connected_flag=True #set flag
        print("connected OK")
        client.subscribe(topic)
    elif client.connected_flag:
        pass
    else:
        print("Bad connection Returned code=",rc)
#    print "connected"
#    client.subscribe(topic)

def dis_con (*args, **kargs):
    print "disconnected"

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    try:
        m_in=(json.loads(msg.payload)) #decode json data
        print m_in
        if 'Value' in m_in:
            name = msg.topic[7:]
#            print 'Name: ', name
#            print 'Value: ', float(m_in['Value'])
            broadcast_input_value('MQTT.' + name, float(m_in['Value']))
    except ValueError:
        print("no json code")

mqtt.Client.connected_flag=False
client = None
topic = "Inputs/ESP/#"
ipaddress = constants.mqtt_.server
port = 1883



def main():
    global client, topic, ipaddress, port

#    if len(sys.argv) == 3:
#        address = sys.argv[1]
#        ipaddress = address.split(":")[0]
#        port = address.split(":")[1]
#        topic = sys.argv[2]
#    else:
#        print "Usage : %r [ipaddress:port] [topic]" % sys.argv[0]
#        exit(1)

    connect(ipaddress, port)


if __name__ == "__main__":
    topic = "Inputs/#"
    ipaddress = '127.0.0.1'
    main()