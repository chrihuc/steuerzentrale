#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:51:19 2018

@author: christooph
"""
import time
from database import mysql_connector as msqc
from outputs.mqtt_publish import mqtt_pub

import constants


"""
 0 Aus  5min
 1 An   5min
 2 Aus  10min
 3 An   10min
 4 Aus  30min
 5 An   30min
 6 Aus  2 h
"""
def main():
    while constants.run:
        try:
            if False:
                # AUS und 5 min Warten
                mqtt_pub("Outputs/Kerze1", '0')

            elif msqc.settings_r()['Nacht'] != 'True' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 5:
                # AN und 5 min Warten
                mqtt_pub("Outputs/Kerze1", '1')
                # Nachtlicht Aus und 5 min Warten
                mqtt_pub("Outputs/Nachtlicht", '0')
            elif msqc.settings_r()['Nacht'] != 'True' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 30:
                # AN und 10 min Warten
                mqtt_pub("Outputs/Kerze1", '3')
                # Nachtlicht Aus und 10 min Warten
                mqtt_pub("Outputs/Nachtlicht", '2')
            elif msqc.settings_r()['Nacht'] != 'True' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 300:
                # AUS und 10 min Warten
                mqtt_pub("Outputs/Kerze1", '2')
                # Nachtlicht Aus und 30 min Warten
                mqtt_pub("Outputs/Nachtlicht", '4')
            elif msqc.settings_r()['Nacht'] != 'True':
                # AUS und 30 min Warten
                mqtt_pub("Outputs/Kerze1", '4')
                # Nachtlicht Aus und 30 min Warten
                mqtt_pub("Outputs/Nachtlicht", '4')
    #        elif False:
    #            # AN und 30 min Warten
    #            client.publish("Outputs/Kerze1", 5, qos=1)

    #        elif False:
    #            # AUS und 2 h Warten
    #            client.publish("Outputs/Kerze1", 6, qos=1)

    #        elif False:
    #            # AN und 2 h Warten
    #            client.publish("Outputs/Kerze1", 7, qos=1)

            elif msqc.settings_r()['Nacht'] == 'True' and int(msqc.settings_r()['V00WOH1RUM1HE01']) < 30:
                # AUS und 6 h Warten
                mqtt_pub("Outputs/Kerze1", '4')
                # Nachtlicht An und 10 min Warten
                mqtt_pub("Outputs/Nachtlicht", '3')
            elif msqc.settings_r()['Nacht'] == 'True':
                # AUS und 6 h Warten
                mqtt_pub("Outputs/Kerze1", '4')
                # Nachtlicht Aus und 10 min Warten
                mqtt_pub("Outputs/Nachtlicht", '3')
    #        elif False:
    #            # AN und 6 h Warten
    #            client.publish("Outputs/Kerze1", 9, qos=1)

            else:
                mqtt_pub("Outputs/Kerze1", '10')

            time.sleep(20)
        except:
            print('Batswitch mqtt next try')