#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: christoph
"""

import paho.mqtt.client as mqtt
import sys
import logging
import constants


def connect(ipaddress, port):
    global client
    client = mqtt.Client()
    assign_handlers(on_connect, on_message)
    client.connect(ipaddress, port, 60)
    client.loop_forever()


def assign_handlers(connect, message):
    """

    :param mqtt.Client client:
    :param connect:
    :param message:
    :return:
    """

    global client
    client.on_connect = connect
    client.on_message = message


def on_connect(client_data, userdata, flags, rc):
    global client, topic
    log.debug("Connected! Subscribing to topic %r" % topic)
    client.subscribe(topic)


def on_message(client_data, userdata, msg):
    global client, topic

    log.debug("Event received: %r :  %r" % (msg.topic, msg.payload))

client = None
topic = ""
ipaddress = ""
port = ""
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def main():
    global client, topic, ipaddress, port

    if len(sys.argv) == 3:
        address = sys.argv[1]
        ipaddress = address.split(":")[0]
        port = address.split(":")[1]
        topic = sys.argv[2]
    else:
        print "Usage : %r [ipaddress:port] [topic]" % sys.argv[0]
        exit(1)

    log.debug("Connecting to %r:%r" % (ipaddress, port))
    connect(ipaddress, port)


if __name__ == "__main__":
    main()