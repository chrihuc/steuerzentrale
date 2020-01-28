# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:18:02 2020

@author: hc
"""

import sys
import constants
sys.path.append(constants.pmatic_folder)

import pmatic

import time
from tools import toolbox
#pmatic.logging(pmatic.DEBUG)

ccu = pmatic.CCU(address=constants.ccu2.hostname, credentials=(constants.ccu2.username, constants.ccu2.password))



#print("%s: %s, Mode: %s" % (device.name, device.summary_state, device.control_mode))
#device.set_temperature = 22.5
#device.control_mode = "MANUAL"
#print("%s: %s, Mode: %s" % (device.name, device.summary_state, device.control_mode))

# adresse: CCU.device_name

# tableheaders : set_temperature | control_mode

def set_device(data_ev, adress):
#       TODO do threaded with stop criteria
#        TODO change to send address and check if connected
#    toolbox.log(data_ev)
    print(data_ev)
    command = data_ev.get('Value')
    deviceName = adress.split(".")[1]
    deviceName = "HM-RCV-50 BidCoS-RF"
    device = list(ccu.devices.query(device_name=deviceName))[0]
    device.values["PRESS_SHORT"].set(True)
    print("pressed")


def receive_communication(payload, *args, **kwargs):
    print(payload, kwargs)
#    toolbox.log(toolbox.kw_unpack(kwargs,'typ') == 'output', toolbox.kw_unpack(kwargs,'receiver') == 'CCU')
    if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'CCU':
        result = set_device(payload, adress=toolbox.kw_unpack(kwargs,'adress'))
        toolbox.communication.send_message(payload, typ='return', value=result)
   
def main():     
    toolbox.communication.register_callback(receive_communication) 
    while True:
        time.sleep(1)     