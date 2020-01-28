# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 21:50:59 2020

@author: hc
"""

import sys
import constants
sys.path.append(constants.pmatic_folder)

import pmatic
#pmatic.logging(pmatic.DEBUG)


ccu = pmatic.CCU(
    address=constants.ccu2.hostname,
    credentials=(constants.ccu2.username, constants.ccu2.password),
    connect_timeout=5,
)

# This function is executed on each state change
def print_summary_state(param):
    # Format the time of last change for printing
#    last_changed = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(param.last_changed))
#    print("%s %s %s" % (last_changed, param.channel.device.name, param.channel.summary_state))
    print("%s %s" % (param.channel.device.name, param.channel.summary_state))
    print(param.channel.device.channels[1].values)
    
def main():
    # Get all HM-Sec-SC (shutter contact) devices
    devices = ccu.devices.query()#device_type="HM-RCV-50")  
    print(list(devices)[0].name)      
    # Register event handler for all grouped devices. It is possible to register to device
    # specific events like on_closed and on_opend or generic events like on_value_changed:
    #devices.on_opend(print_summary_state)
    #devices.on_closed(print_summary_state)
#    devices.on_value_changed(print_summary_state)
    devices.on_value_updated(print_summary_state)
    
    num_sensors = len(devices)
    if False: #not num_sensors:
        print("Found no sensors. Terminating.")
    else:
        print("Found %d sensors. Waiting for changes..." % num_sensors)
    
        ccu.events.init()
    
        # Now wait for changes till termination of the program
        # ccu.events.wait()
        try:
            while ccu.events._server.is_alive() and constants.run:
                time.sleep(1)
        except KeyboardInterrupt:
            ccu.events._server.stop()
            ccu.events._server.join()                
        ccu.events.close()    
    
if __name__ == "__main__":
    main()    