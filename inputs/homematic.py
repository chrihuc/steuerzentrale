# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 21:50:59 2020

@author: hc
"""

import constants
import sys

import time
from pyhomematic import HMConnection
from tools import toolbox


def systemcallback(src, *args):
#    pass
    print(src)
#    for arg in args:
#        print(arg)
   

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
#    toolbox.log(Name, Value, level=9)
    toolbox.communication.send_message(payload, typ='InputValue')

def eventcallback(address, interface_id, key, value):
    keys = ['LOWBAT', 'STATE', 'LEVEL', 'ACTUAL_TEMPERATURE', 'OPERATING_VOLTAGE', 'SET_TEMPERATURE', 'SET_POINT_TEMPERATURE', 'PRESS_SHORT', 'PRESS_LONG',
            'HUMIDITY', 'ILLUMINATION', 'WIND_SPEED', 'LOW_BAT', 'MOTION']
#    print("CALLBACK: %s, %s, %s, %s" % (address, interface_id, key, value))
    if key in keys:
#        print("CALLBACK: %s, %s, %s, %s" % (address, interface_id, key, value)) 
        broadcast_input_value('homematic.' + address + '.' + key, float(value))
    else:
        pass
#        print(address, interface_id, key, value)

def main():
    pyhomematic = HMConnection(interface_id="myserver",
                               autostart=True,
                               eventcallback=systemcallback,
                               remotes={"rf":{
                                   "ip":constants.ccu2.hostname,
                                   "port": 2001},
							   "ip":{
                                   "ip":constants.ccu2.hostname,
                                   "port": 2010}},
                            rpcusername=constants.ccu2.username, rpcpassword=constants.ccu2.password)
    
    sleepcounter = 0
    while sleepcounter < 20: #not pyhomematic.devices and
        #print("Waiting for devices")
        sleepcounter += 1
        time.sleep(1)
    print(pyhomematic.devices)  
    
    # Set an eventcallback for the doorcontact that should be called when events occur.
    for device, value in pyhomematic.devices.items():
    	for items, ivalues in value.items():
    		print(items)
    		try:
    			ivalues.setEventCallback(eventcallback)
    			print("done")
    		except:
    			pass
    # Now open / close doorcontact and watch the eventcallback being called.
    
#    print(pyhomematic._server.getAllSystemVariables())
    
    try:
        while constants.run:
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    
    # Stop the server thread so Python can exit properly.
    pyhomematic.stop()
    sys.exit(0)  
    
if __name__ == "__main__":
    main()    
