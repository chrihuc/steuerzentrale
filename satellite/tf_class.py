#!/usr/bin/env python
# -*- coding: utf-8 -*-  

PORT = 4223

from functools import partial

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16 import IO16
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_moisture import Moisture
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_distance_us import BrickletDistanceUS
from threading import Timer
import time
import datetime

import tifo_config
import constants

from socket import socket, AF_INET, SOCK_DGRAM

mySocket = socket( AF_INET, SOCK_DGRAM )


class io16Dict:
    def __init__(self):
        self.liste = []

    def addIO(self, IO,addr, length):
        dicti = {}
        dicti["IO"] = IO
        dicti['addr'] = addr
        dicti["value"] = 0
        dicti["valueA"] = 0
        dicti["valueB"] = 0
        times = []
        for cnt in range(0,length):
            times.append(datetime.datetime.now())
        dicti["times"] = times
        self.liste.append(dicti)

    def setValues(self, IO,  values, port = 'a'):
        for ios in self.liste:
            if ios.get('IO') == IO:
                if port == 'a':
                    ios["valueA"] = values
                else:
                    ios["valueB"] = values
                
    def setTime(self, IO,  addr, port = 'a'):
        for ios in self.liste:
            if ios.get('IO') == IO:        
                index = int(log2(addr))
                times = ios.get("times")
                times[index] = datetime.datetime.now()
                ios["times"] = times
                
    def getTimeDiff(self, IO,  addr, port = 'a'):
        for ios in self.liste:
            if ios.get('IO') == IO:        
                index = int(log2(addr))
                times = ios.get("times")
                timedelta = datetime.datetime.now() - times[index]
                #times[index] = 0
                ios["times"] = times     
                return timedelta
        
class tiFo:
    def __init__(self):
        self.led = None
        self.io = []
        self.io16list = io16Dict()
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
        self.ipcon.connect(constants.ownIP, PORT) 
        #self.ipcon.enumerate()        
        

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
        name = tifo_config.inputs.get(str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]))
        dicti['value'] = str(illuminance)
        dicti['name'] = name
        print dicti
        mySocket.sendto(str(dicti) ,(constants.server1,constants.broadPort))

    def cb_interrupt(self, port, interrupt_mask, value_mask, device):
#        print('Interrupt on port: ' + port + str(bin(interrupt_mask)))
#        print('Value: ' + str(bin(value_mask)))
        temp_uid = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        name = tifo_config.IO16i.get(temp_uid).get(port + str(bin(interrupt_mask)))
        if port == 'a':
            nc_mask = tifo_config.IO16.get(temp_uid)[7]
        else:
            nc_mask = tifo_config.IO16.get(temp_uid)[8]
        value = (value_mask&interrupt_mask)/interrupt_mask
        nc_pos = (nc_mask&interrupt_mask)/interrupt_mask
        dicti = {}
        dicti['name'] = name
        #print name, value
        self.io16list.setValues(device,value_mask,port)
        #print self.io16list.getTimeDiff(device,interrupt_mask, port)
        if value == nc_pos:        
            dicti['value'] = self.io16list.getTimeDiff(device,interrupt_mask, port)
        else:
            dicti['value'] = 0
            self.io16list.setTime(device,interrupt_mask, port)
        print dicti
        #mySocket.sendto(str(dicti) ,(constants.server1,constants.broadPort))       

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
                self.io.append(IO16(uid, self.ipcon))
                temp_uid = str(self.io[-1].get_identity()[1]) +"."+ str(self.io[-1].get_identity()[0])
                self.io16list.addIO(self.io[-1],temp_uid,16)
                self.io[-1].set_debounce_period(100)
                if tifo_config.IO16.get(temp_uid) <> None:
                    self.io[-1].set_port_interrupt('a', tifo_config.IO16.get(temp_uid)[0])
                    self.io[-1].set_port_interrupt('b', tifo_config.IO16.get(temp_uid)[1])
                    self.io[-1].set_port_configuration('a', tifo_config.IO16.get(temp_uid)[0],'i',True)
                    self.io[-1].set_port_configuration('b', tifo_config.IO16.get(temp_uid)[1],'i',True)                    
                    self.io[-1].set_port_configuration('a', tifo_config.IO16.get(temp_uid)[2],'o',False)
                    self.io[-1].set_port_configuration('b', tifo_config.IO16.get(temp_uid)[3],'o',False)
                    self.io[-1].set_port_monoflop('a', tifo_config.IO16.get(temp_uid)[4],0,tifo_config.IO16.get(temp_uid)[6])
                    self.io[-1].set_port_monoflop('b', tifo_config.IO16.get(temp_uid)[5],0,tifo_config.IO16.get(temp_uid)[6])
                    self.io[-1].register_callback(self.io[-1].CALLBACK_INTERRUPT, partial( self.cb_interrupt, device = self.io[-1] ))
             
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
                self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, lambda event1, event2, event3, args=args: self.cb_ambLight(event1, event2, event3, args))
                
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
        self.ipcon.connect(constants.ownIP, PORT) 
        #self.ipcon.enumerate()                 
       
    
    def cb_reached_vc(self):        
        voltage = self.vc.get_voltage()
        dicti = {}
        dicti['value'] = str(voltage)
        dicti['name'] = 'Voltage'
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort)) 
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort)) 
        current = self.vc.get_current()
        dicti = {}
        dicti['value'] = str(current)
        dicti['name'] = 'Current'
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort)) 
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort))         
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
        self.ipcon.connect(constants.ownIP, PORT) 
        #self.ipcon.enumerate()                 
       
    
    def cb_distance(self, distance):        
        dicti = {}
        dicti['value'] = str(distance)
        dicti['name'] = str(self.dus.get_identity()[0]) + "_" + str(self.dus.get_identity()[5])
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort)) 
        mySocket.sendto(str(dicti),(constants.server1,constants.broadPort)) 
       
    
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
