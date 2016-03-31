#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "192.168.192.81"
PORT = 4223
SERVER_IP_1   = '192.168.192.10'
SERVER_IP_2   = '192.168.192.33'
OUTPUTS_PORT = 5000

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16 import IO16
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_moisture import Moisture
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_distance_us import BrickletDistanceUS
from threading import Timer
import time

from socket import socket, AF_INET, SOCK_DGRAM

mySocket = socket( AF_INET, SOCK_DGRAM )

uebersetzung = {'63mHZj.m4d':'V01ZIM1RUM1HE01'}

class tiFo:
    def __init__(self):
        self.led = None
        self.io = None
        self.al = []
        self.moist = None
        # Create IP Connection
        self.ipcon = IPConnection() 
        # Register IP Connection callbacks
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, 
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, 
                                     self.cb_connected)
        # Connect to brickd, will trigger cb_connected
        self.ipcon.connect(HOST, PORT) 
        self.ipcon.enumerate()        
        

    def cb_ambLight(self, illuminance,device):
        thresUp = illuminance * 4/3
        thresDown = illuminance * 4 / 5
        if thresDown == 0:
            thresDown = 0
            thresUp = 3
        if thresUp > 9000:
            thresUp = 9000            
        print illuminance, thresDown, thresUp
        device.set_illuminance_callback_threshold('o', thresDown, thresUp)
        dicti = {}
        name = uebersetzung.get(str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]))
        dicti['value'] = str(illuminance)
        dicti['name'] = name
        print dicti
        mySocket.sendto(str(dicti) ,('192.168.192.81',OUTPUTS_PORT))        

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):
        #global self.led
        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            # Enumeration for LED
            if device_identifier == LEDStrip.DEVICE_IDENTIFIER:
                self.led = LEDStrip(uid, self.ipcon)
                self.led.set_chip_type(2812)
                self.led.set_frame_duration(50)
                #self.led.register_callback(self.led.CALLBACK_FRAME_RENDERED, 
                #                lambda x: __cb_frame_rendered__(self.led, x))
                #self.led.set_rgb_values(0, self.NUM_LEDS, self.r, self.g, self.b)
                #self.led.set_rgb_values(15, self.NUM_LEDS, self.r, self.g, self.b)
                #self.led.set_rgb_values(30, self.NUM_LEDS, self.r, self.g, self.b)

            if device_identifier == IO16.DEVICE_IDENTIFIER:
                self.io = IO16(uid, self.ipcon)
                self.io.set_debounce_period(500)
                self.io.set_port_interrupt('a', 0b00111111)
                self.io.register_callback(self.io.CALLBACK_INTERRUPT, self.cb_interrupt)
             
            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.al.append(AmbientLight(uid, self.ipcon))
                self.al[-1].set_illuminance_callback_threshold('o', 0, 0)
                self.al[-1].set_debounce_period(100)
                #self.al.set_illuminance_callback_threshold('<', 30, 30)
                #self.al.set_analog_value_callback_period(10000)
                #self.al.set_illuminance_callback_period(10000)
                #self.al.register_callback(self.al.CALLBACK_ILLUMINANCE, self.cb_ambLight)
                #self.al.register_callback(self.al.CALLBACK_ILLUMINANCE_REACHED, self.cb_ambLight)
                args = self.al[-1]
                self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, lambda event, args=args: self.cb_ambLight(event,args))
                
            if device_identifier == Moisture.DEVICE_IDENTIFIER:
                self.moist = Moisture(uid, self.ipcon)
                self.moist.set_moisture_callback_period(10000)
                self.moist.register_callback(self.moist.CALLBACK_MOISTURE, self.cb_moisture)

        
    def cb_connected(self, connected_reason):
        # Enumerate devices again. If we reconnected, the Bricks/Bricklets
        # may have been offline and the configuration may be lost.
        # In this case we don't care for the reason of the connection
        self.ipcon.enumerate()     

class volt_cur:
    def __init__(self):
        self.vc = None

        # Create IP Connection
        self.ipcon = IPConnection() 

        # Register IP Connection callbacks
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, 
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, 
                                     self.cb_connected)

        # Connect to brickd, will trigger cb_connected
        self.ipcon.connect(HOST, PORT) 
        #self.ipcon.enumerate()                 
       
    
    def cb_reached_vc(self):        
        voltage = self.vc.get_voltage()
        dicti = {}
        dicti['value'] = str(voltage)
        dicti['name'] = 'Voltage'
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT)) 
        current = self.vc.get_current()
        dicti = {}
        dicti['value'] = str(current)
        dicti['name'] = 'Current'
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT))         
        thread_cb_reached = Timer(60, self.cb_reached_vc, [])
        thread_cb_reached.start()        
       
    
    # Callback handles device connections and configures possibly lost 
    # configuration of lcd and temperature callbacks, backlight etc.
    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):

        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            
            # Enumeration for V/C
            if device_identifier == BrickletVoltageCurrent.DEVICE_IDENTIFIER:
                self.vc = BrickletVoltageCurrent(uid, self.ipcon)
                self.cb_reached_vc()
        
    def cb_connected(self, connected_reason):
        # Enumerate devices again. If we reconnected, the Bricks/Bricklets
        # may have been offline and the configuration may be lost.
        # In this case we don't care for the reason of the connection
        self.ipcon.enumerate()    
        
class dist_us:
    def __init__(self):
        self.dus = None

        # Create IP Connection
        self.ipcon = IPConnection() 

        # Register IP Connection callbacks
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, 
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, 
                                     self.cb_connected)

        # Connect to brickd, will trigger cb_connected
        self.ipcon.connect(HOST, PORT) 
        #self.ipcon.enumerate()                 
       
    
    def cb_distance(self, distance):        
        dicti = {}
        dicti['value'] = str(distance)
        dicti['name'] = str(self.dus.get_identity()[0]) + "_" + str(self.dus.get_identity()[5])
        mySocket.sendto(str(dicti),(SERVER_IP_1,OUTPUTS_PORT)) 
        mySocket.sendto(str(dicti),(SERVER_IP_2,OUTPUTS_PORT)) 
       
    
    # Callback handles device connections and configures possibly lost 
    # configuration of lcd and temperature callbacks, backlight etc.
    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):

        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            
            # Enumeration for Distance US
            if device_identifier == BrickletDistanceUS.DEVICE_IDENTIFIER:
                self.dus = BrickletDistanceUS(uid, self.ipcon)
                self.dus.register_callback(self.dus.CALLBACK_DISTANCE, self.cb_distance)
                self.dus.set_distance_callback_period(10000)

        
    def cb_connected(self, connected_reason):
        # Enumerate devices again. If we reconnected, the Bricks/Bricklets
        # may have been offline and the configuration may be lost.
        # In this case we don't care for the reason of the connection
        self.ipcon.enumerate()          
        
    
if __name__ == "__main__":
    #sb = dist_us()
    tf = tiFo()
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
