#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 08:36:11 2020

@author: christoph
"""

import requests
from bs4 import BeautifulSoup
import json
from tools import toolbox
from outputs import mqtt_publish
import constants
import time
import copy

class Shelly(object):

    DEFAULT_PORT = 80
    HEADERS = {}
    PUT_HEADERS = {'content-type': 'application/json'}
    
    def __init__(self, hostname=None, port=DEFAULT_PORT):
        self.hostname = hostname
        self.port = port
        self.cookies = dict()        
    
    def get_shelly(self):
        response = requests.get(self.__build_uri_for_path__("/shelly"),
#                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json() 
    
    def get_login(self):
        response = requests.get(self.__build_uri_for_path__("/settings/login"),
#                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json()    
    
    def set_login(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = requests.put(self.__build_uri_for_path__("/settings/login"),
#                      headers=Secvest.PUT_HEADERS,
                      data=json.dumps(data),
                      cookies=self.cookies,
                      verify=False)
        return response       
    
    def get_settings(self, nr=0):
        response = requests.get(self.__build_uri_for_path__("/settings/relay/" + str(nr)),
#                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json()     
    
    def set_setting(self, data, channel="/settings/relay/0"):
        response = requests.post(self.__build_uri_for_path__(channel),
#                      headers=Secvest.PUT_HEADERS,
                      data=data,
                      cookies=self.cookies,
                      verify=False)
        return response    
    
    def __build_base_uri__(self):
        return 'http://%s:%i' % (self.hostname, self.port) 
    
    def __build_uri_for_path__(self, path):
        return self.__build_base_uri__() + path    
    
def main():
#    shelly = Shelly("192.168.193.201")
#    print(shelly.set_login())
#    print(shelly.get_login())
#    print(shelly.get_settings())
    
#    sw_toggle = {'btn_type': 'detached'}
#    print(shelly.set_setting(sw_toggle))
#    print(shelly.get_settings())    
#    sw_toggle = {'btn_type': 'toggle'}
#    shelly.set_setting(sw_toggle)
#    print(shelly.get_settings())  
    while constants.run:
        time.sleep(1)      

def receive_communication(payload, *args, **kwargs):
    if toolbox.kw_unpack(kwargs,'typ') == 'output' and (toolbox.kw_unpack(kwargs,'receiver') in ['Shelly', 'ShellyConf', 'ShellyDim', 'WLED']):
        adress=toolbox.kw_unpack(kwargs,'adress')
        device = adress.split(".")[1]
        ip = None
        try:
            ip = adress.split(".")[3]
            ip = ip.replace(":", ".")
        except:
            pass
#        print(payload)
#            der teil muss abgekürzt werden, wenn ein ESP der empfänger ist, auf nur das nötigste
#        einschalten der shelly switches scheint nur über channel zu gehen
        if toolbox.kw_unpack(kwargs,'receiver') == 'Shelly' and toolbox.kw_unpack(payload, 'Channel', None) is None:
            if payload['Value'] == 'pulse_open':
                result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], 'open', retain=False)
                toolbox.communication.send_message(payload, typ='return', value=result) 
                time.sleep(0.3)
                result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], 'stop', retain=False)
                toolbox.communication.send_message(payload, typ='return', value=result)    
            elif payload['Value'] == 'pulse_close':
                result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], 'close', retain=False)
                toolbox.communication.send_message(payload, typ='return', value=result) 
                time.sleep(0.3)
                result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], 'stop', retain=False)
                toolbox.communication.send_message(payload, typ='return', value=result)                  
            else:
                result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], payload['Value'], retain=False)
                toolbox.communication.send_message(payload, typ='return', value=result) 
        elif toolbox.kw_unpack(kwargs,'receiver') == 'Shelly' and payload['Channel'] is not None and ip is not None:
            shelly = Shelly(ip) 
            shelly.set_setting(payload['Value'], payload['Channel'])            
        elif toolbox.kw_unpack(kwargs,'receiver') == 'ShellyDim':
            result = mqtt_publish.mqtt_pub("shellies/" + device + adress.split(".")[2], payload, retain=False)
            toolbox.communication.send_message(payload, typ='return', value=result)             
        elif toolbox.kw_unpack(kwargs,'receiver') == 'ShellyConf':
            ip = adress.split(".")[1] + "." + adress.split(".")[2] + "." + adress.split(".")[3] + "." + adress.split(".")[4]
            shelly = Shelly(ip)
            sw_toggle = {'btn_type': payload['Value']}
            shelly.set_setting(sw_toggle)    
            
        elif toolbox.kw_unpack(kwargs,'receiver') == 'WLED':
#            print(device)
#            print(payload)
#            pscopy = copy.copy(payload)
            #pscopy.pop('bri', None)
            uhr = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
            result = False
#            print(uhr, payload)
            payload.pop('Device', None)
            payload.pop('Szene', None)
            payload.pop('Szene_id', None)
            payload.pop('Id', None)
            payload.pop('Name', None)
            payload.pop('ts', None)            
            if 'bri' in payload and not payload['bri']:
                payload.pop('bri', None)
                result = mqtt_publish.mqtt_pub(device + "/api", payload, retain=True, short=True)
#                print(uhr, payload)
            elif 'bri' in payload and payload['bri'] and int(payload['bri']) > 0:
                payload['bri'] = round(payload['bri'])   
                #payload.pop('ps', None)
                #payload['on'] = True    
                
                result = mqtt_publish.mqtt_pub(device + "/api", payload, short=True)
#                print(uhr, payload)
            elif 'bri' in payload and payload['bri'] and int(payload['bri']) <= 0:
                payload['bri'] = 0  
                #payload.pop('ps', None)
                #payload['on'] = False    
                result = mqtt_publish.mqtt_pub(device + "/api", payload, short=True)         
#                print(uhr, payload)
                
            toolbox.communication.send_message(payload, typ='return', value=result)                
    

toolbox.communication.register_callback(receive_communication)
    
if __name__ == "__main__":
    main()