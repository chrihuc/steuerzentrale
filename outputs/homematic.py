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
    #       TODO do threaded with stop criteria
    #        TODO change to send address and check if connected
    #    toolbox.log(data_ev)
        print(data_ev)
        value = data_ev.get('Value')
        deviceName = adress.split(".")[1]
        command = adress.split(".")[2]
#        deviceName = "HM-RCV-50 BidCoS-RF"
#        device = list(ccu.devices.query(device_name=deviceName))[0]
#        device.values["PRESS_SHORT"].set(True)
        if command == 'set_level':
            self.pyhomematic.devices[deviceName].set_level(value)
        elif command == 'set_temperature':
            self.pyhomematic.devices[deviceName].set_temperature(value)            
#        print("pressed")
    
    
    def receive_communication(self, payload, *args, **kwargs):
    #    toolbox.log(toolbox.kw_unpack(kwargs,'typ') == 'output', toolbox.kw_unpack(kwargs,'receiver') == 'CCU')
    # Adress = CCU.001198A99FB4CD:1.set_temperature
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'CCU':
#            print(payload, kwargs)
            result = self.set_device(payload, adress=toolbox.kw_unpack(kwargs,'adress'))
            toolbox.communication.send_message(payload, typ='return', value=result)
   
def main(): 
    try:
        hm = HM_out() 
        while constants.run:
            time.sleep(1)
    except:
        pass
#        print('interrupted!')    
        
if __name__ == "__main__":
    main()           
#else:
#    t = toolbox.OwnTimer(0, function=main, args = [], name="homematic")
#    t.start()        