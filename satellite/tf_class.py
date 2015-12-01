#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
SERVER_IP_1   = '192.168.192.10'
SERVER_IP_2   = '192.168.192.33'
OUTPUTS_PORT = 5000

from tinkerforge.ip_connection import IPConnection
#from tinkerforge.bricklet_io16 import IO16
#from tinkerforge.bricklet_led_strip import LEDStrip
#from tinkerforge.bricklet_ambient_light import AmbientLight
#from tinkerforge.bricklet_moisture import Moisture
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from threading import Timer
import time

from socket import socket, AF_INET, SOCK_DGRAM

mySocket = socket( AF_INET, SOCK_DGRAM )

class TiFo_SideB:
    HOST = "localhost"
    PORT = 4223

    NUM_LEDS = 15

    r = [0]*16
    g = [0]*16
    b = [0]*16
    r_index = 0 
    r_start = 0
    zufall = False
    
    def __cb_frame_rendered__(self, led_strip, length):
        global r_index
        b[r_index] = 0
        if r_index == NUM_LEDS-1:
            r_index = 0
        else:
            r_index += 1

        b[r_index] = 255

        # Set new data for next render cycle
        led_strip.set_rgb_values(0, NUM_LEDS, r, g, b)
        
    def __init__(self):
        self.led = None
        self.io = None
        self.al = None
        self.moist = None
        self.vc = None

        # Create IP Connection
        self.ipcon = IPConnection() 

        # Register IP Connection callbacks
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, 
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, 
                                     self.cb_connected)

        # Connect to brickd, will trigger cb_connected
        self.ipcon.connect(TiFo_SideB.HOST, TiFo_SideB.PORT) 
        self.ipcon.enumerate()                 
       
    
    def cb_reached(self):        
        voltage = self.vc.get_voltage()
        dicti = {}
        dicti['value'] = str(illuminance)
        dicti['name'] = 'Voltage'
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT)) 
        thread_cb_reached = Timer(60, self.cb_reached, [])
        thread_cb_reached.start()        

    def cb_interrupt(self, port, interrupt_mask, value_mask):
        #print('Interrupt on port: ' + port + str(bin(interrupt_mask)))
        #print('Value: ' + str(bin(value_mask)))
        dicti = {}
        dicti['value'] = str((interrupt_mask & value_mask))
        dicti['name'] = port + str((interrupt_mask))      
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT))        
    
    # Callback handles device connections and configures possibly lost 
    # configuration of lcd and temperature callbacks, backlight etc.
    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):

        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            
            # Enumeration for V/C
            if device_identifier == BrickletVoltageCurrent.DEVICE_IDENTIFIER:
                self.vc = BrickletVoltageCurrent(uid, self.ipcon)
                self.cb_reached()

        
    def cb_connected(self, connected_reason):
        # Enumerate devices again. If we reconnected, the Bricks/Bricklets
        # may have been offline and the configuration may be lost.
        # In this case we don't care for the reason of the connection
        self.ipcon.enumerate()      
        
    
if __name__ == "__main__":
    sb = TiFo_SideB()
    
    raw_input('Press key to exit\n') # Use input() in Python 3   
    #sb.set_one_color(rot = 255)
    #raw_input('Press key to exit\n')   
    #time.sleep(15)
    #sb.flash(start = 0, new = True, n_blau = 255) 
    #sb.flash(start = 15, new = True, n_blau = 255)
    #sb.flash(start = 30, new = True, n_blau = 255)
    #sb.flash(start = 30, new = True, reverse = True, n_gruen = 255)
    #sb.flash(start = 15, new = True, reverse = True, n_gruen = 255)
    #sb.flash(start = 0, new = True, reverse = True, n_gruen = 255)    
    #raw_input('Press key to exit\n') 
    #ipcon.disconnect()
