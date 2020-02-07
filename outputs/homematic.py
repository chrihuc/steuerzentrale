# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:18:02 2020

@author: hc
"""

import constants
from pyhomematic import HMConnection


import time
from tools import toolbox

# pyhomematic.devices[DEVICE1].set_level(0.5)

class HM_out():
    def __init__(self):
        self.pyhomematic = HMConnection(interface_id="myserver",
                           autostart=True,
                           systemcallback=self.systemcallback,
                           remotes={"rf":{
                               "ip":constants.ccu2.hostname,
                               "port": 2001},
							   "ip":{
                               "ip":constants.ccu2.hostname,
                               "port": 2010}})
        toolbox.communication.register_callback(self.receive_communication) 
    

    def systemcallback(self, src, *args):
        pass    
    
    def set_device(self, data_ev, adress):
        value = data_ev.get('Value')
        if not value:
            value = data_ev.get('Szene')
        deviceGroup = adress.split(".")[1]
        deviceName = adress.split(".")[2]        
        command = adress.split(".")[3]

        if command == 'set_level':
            self.pyhomematic.devices[deviceName].set_level(value)
        elif command == 'set_temperature':
#            print(deviceGroup, deviceName, value)
            self.pyhomematic.devices[deviceGroup][deviceName].set_temperature(value)

    
    
    def receive_communication(self, payload, *args, **kwargs):
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'CCU':
            result = self.set_device(payload, adress=toolbox.kw_unpack(kwargs,'adress'))
            toolbox.communication.send_message(payload, typ='return', value=result)
   
def main(): 
    try:
        hm = HM_out() 
        while constants.run:
            time.sleep(1)
    except:
        pass    
        
if __name__ == "__main__":
    main()           
     