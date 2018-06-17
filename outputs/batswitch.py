#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:51:19 2018

@author: christooph
"""
import time
import paho.mqtt.client as mqtt
from database import mysql_connector as msqc

import constants

client = mqtt.Client(constants.name)
client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
client.connect(constants.mqtt_.server)
client.loop_start()

def main():
    while constants.run:
        try:
            print msqc.settings_r()['V00WOH1RUM1HE01']
            if False:
                # AUS und 5 min Warten
                client.publish("Outputs/Kerze1", 0, qos=1)
#                print '0'
            elif msqc.settings_r()['Status'] != 'Schlafen' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 5:
                # AN und 5 min Warten
                client.publish("Outputs/Kerze1", 1, qos=1)
#                print '1'
            elif msqc.settings_r()['Status'] != 'Schlafen' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 30:
                # AN und 10 min Warten
                client.publish("Outputs/Kerze1", 3, qos=1)
#                print '3'
            elif msqc.settings_r()['Status'] != 'Schlafen' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 300:
                # AUS und 10 min Warten
                client.publish("Outputs/Kerze1", 2, qos=1)
#                print '2'
            elif msqc.settings_r()['Status'] != 'Schlafen':
                # AUS und 30 min Warten
                client.publish("Outputs/Kerze1", 4, qos=1)
#                print '4'
    #        elif False:
    #            # AN und 30 min Warten
    #            client.publish("Outputs/Kerze1", 5, qos=1)
    #            print '5'
    #        elif False:
    #            # AUS und 2 h Warten
    #            client.publish("Outputs/Kerze1", 6, qos=1)
    #            print '6'
    #        elif False:
    #            # AN und 2 h Warten
    #            client.publish("Outputs/Kerze1", 7, qos=1)
    #            print '7'
            elif msqc.settings_r()['Status'] == 'Schlafen':
                # AUS und 6 h Warten
                client.publish("Outputs/Kerze1", 8, qos=1)
#                print '8'
    #        elif False:
    #            # AN und 6 h Warten
    #            client.publish("Outputs/Kerze1", 9, qos=1)
    #            print '9'
            else:
                client.publish("Outputs/Kerze1", 10, qos=1)
#                print '10'
            time.sleep(5)
        except:
            print 'Batswitch mqtt next try'