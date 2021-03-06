# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 18:18:47 2017

@author: chuckle
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

PORT = 4223

from functools import partial

import socket

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16 import IO16
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_moisture import Moisture
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_distance_us import BrickletDistanceUS
from tinkerforge.bricklet_dual_relay import BrickletDualRelay
from tinkerforge.bricklet_co2 import BrickletCO2
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
from tinkerforge.bricklet_ptc import BrickletPTC
from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_barometer import BrickletBarometer
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2
from tinkerforge.brick_master import BrickMaster
from tinkerforge.ip_connection import Error

import threading
#from threading import Timer
import time
from time import localtime,strftime
from math import log
import datetime
import uuid

#from distutils.version import LooseVersion

import constants

# on server:
from tifo import settings
from tifo import pattern_reco as pr
from tools import toolbox
from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value)
    toolbox.communication.send_message(payload, typ='InputValue')

#    on satellite:
#    mySocket.sendto(str(payload) ,(constants.server1,constants.broadPort))

# tranisiton modes
ANSTEIGEND = 0
ABSTEIGEND = 1
ZUSAMMEN = 2
GEMISCHT = 3

class io16Dict:
    def __init__(self):
        self.liste = []

    def addIO(self, IO,addr, length):
        global liste
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
                index = int(log(addr,2))
                times = ios.get("times")
                times[index] = datetime.datetime.now()
                ios["times"] = times

    def getTimeDiff(self, IO,  addr, port = 'a'):
        for ios in self.liste:
            if ios.get('IO') == IO:
                index = int(log(addr,2))
                times = ios.get("times")
                timedelta = datetime.datetime.now() - times[index]
                #times[index] = 0
                ios["times"] = times
                return timedelta.total_seconds()

class LEDStrips:
    def __init__(self):
        self.liste = []

    def addLED(self, LED,addr):
        global liste
        dicti = {}
        dicti["LED"] = LED
        dicti['addr'] = addr
        self.liste.append(dicti)

class TiFo:

    r = [0]*16
    g = [0]*16
    b = [0]*16

    ipcon = None

    led = None
    io = []
    io16list = io16Dict()
    LEDs = []
    LEDList = LEDStrips()
    al = []
    drb = []
    master = []
    md = []
    si = []
    ptc = []
    temp = []
    co2 = []
    moist = None
    unknown = []
    threadliste = []

    def __init__(self, ip):
        self.led = None
        self.io = []
        self.io16list = io16Dict()
        self.LEDs = []
        self.LEDList = LEDStrips()
        self.al = []
        self.drb = []
        self.master = []
        self.md = []
        self.si = []
        self.ptc = []
        self.temp = []
        self.baro = []
        self.humi = []
        self.co2 = []
        self.volcu = []
        self.moist = None
        self.unknown = []
        self.threadliste = []
        self.ip = ip
        self.delay = 5
        self.timeoutTime = 600
        self.timeout = threading.Timer(self.timeoutTime, self.timedOut)

        self.ipcon = IPConnection()
        self.ipcon.set_timeout(10)

        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE,
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED,
                                     self.cb_connected)


    def timeout_reset(self):
        self.timeout.cancel()
        self.timeout = threading.Timer(self.timeoutTime, self.timedOut)
        self.timeout.start()

    def timedOut(self):
        self.connect()

    def connect(self):
        try:
            self.ipcon.disconnect()
        except:
            pass
        # Connect to brickd, will trigger cb_connected
        while True:
            try:
                self.ipcon.connect(self.ip, PORT)
                aes.new_event(description="Tifo connected: "+self.ip, prio=7)
                break
            except Error as e:
                toolbox.log('Connection Error: ' + str(e.description))
                time.sleep(1)
            except socket.error as e:
                toolbox.log('Socket error: ' + str(e))
                time.sleep(1)
        toolbox.communication.register_callback(self.receive_communication)
        time.sleep(5)
        toolbox.log('TiFo started')

    def main(self):
        # Create IP Connection
        self.connect()
        while constants.run:
            toolbox.sleep(600)
#            for t in self.threadliste:
#                if not t in threading.enumerate():
##                    print t.args
##                    new_t = threading.Timer(60, function=t.function, args = t.args)
#                    aes.new_event(description="Thread stopped: "+t.name, prio=1)
#                    new_t = toolbox.OwnTimer(0, name=t.name, function=t.function, args = t.args)
#                    new_t.start()
#                    self.threadliste.remove(t)
#                    self.threadliste.append(new_t)
#                    aes.new_event(description="Restarted Thread: "+t.name, prio=1)



    def thread_RSerror(self):
        while constants.run:
            for mastr in self.master:
                print(mastr.get_rs485_error_log())
            toolbox.sleep(60)

    def cb_ambLight(self, illuminance,device):
        toolbox.log(device)
        thresUp = illuminance * 4/3
        thresDown = illuminance * 4 / 5
        if thresDown == 0:
            thresDown = 0
            thresUp = 3
        if thresUp > 9000:
            thresUp = 9000
        device.set_illuminance_callback_threshold('o', thresDown, thresUp)
        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name, str(illuminance))
        self.timeout_reset()

    def cb_value(self, value,device,div=1.0,ext=''):
        toolbox.log(device)
        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name + ext, str(value/div))
        self.timeout_reset()

    def thread_ambLight(self, device):
        while constants.run:
            toolbox.log(device)
            illuminance = device.get_illuminance()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name, str(illuminance))
            toolbox.sleep(60)

    def thread_CO2(self, device):
        while constants.run:
            toolbox.log(device)
            value = device.get_co2_concentration()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name, str(value))
            toolbox.sleep(60)

    def thread_pt(self, device):
        while constants.run:
            toolbox.log(device)
            toolbox.log("thread_pt", device)
            value = device.get_temperature()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name, str(float(value)/100))
            toolbox.sleep(60)

    def thread_cp(self, device):
        while constants.run:
            toolbox.log(device)
            value = device.get_air_pressure()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name, str(float(value)/1000))
            toolbox.sleep(60)

    def thread_hum(self, device):
        while constants.run:
            toolbox.log(device)
            value = device.get_humidity()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name + '.HU', str(float(value)/100))
            toolbox.sleep(10)
            value = device.get_temperature()
            broadcast_input_value('TiFo.' + name + '.TE', str(float(value)/100))
            toolbox.sleep(60)

    def thread_volc(self, device):
        while constants.run:
            toolbox.log(device)
            value = device.get_voltage()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name + '.U', str(float(value)/1000))
            toolbox.sleep(10)
            value = device.get_current()
            broadcast_input_value('TiFo.' + name + '.I', str(float(value)/100))
            toolbox.sleep(60)

    def cb_volc_vol(self, value, device, uid):
        toolbox.log(device)
        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name + '.U', str(float(value)/1000))
        self.timeout_reset()

    def cb_volc_cur(self, value, device, uid):
        toolbox.log(device)
        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name + '.I', str(float(value)/100))
        self.timeout_reset()

    def cb_interrupt(self, port, interrupt_mask, value_mask, device, uid):
        toolbox.log(device)
        #print('Interrupt on port: ' + port + str(bin(interrupt_mask)))
        #print('Value: ' + str(bin(value_mask)))
        namelist = []
        temp_uid = uid #str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        bit_list = [(1 << bit) for bit in range(7, -1, -1)]
        for wert in bit_list:
            if interrupt_mask & wert > 0:
#                name = settings.IO16i.get(temp_uid).get(port + str(bin(wert)))
                name = temp_uid + "." + port + str(bin(wert))
                if name != None:
                    namelist.append(name)
        if port == 'a':
            nc_mask = settings.IO16.get(temp_uid)[7]
        else:
            nc_mask = settings.IO16.get(temp_uid)[8]
        value = (value_mask&interrupt_mask)/interrupt_mask
        nc_pos = (nc_mask&interrupt_mask)/interrupt_mask
#        dicti = {}
#        dicti['Name'] = name
#        dicti['temp_uid'] = temp_uid
#        dicti['name'] = port + str(bin(interrupt_mask))
        #print name, value
        self.io16list.setValues(device,value_mask,port)
        #print self.io16list.getTimeDiff(device,interrupt_mask, port)
        if value == nc_pos:
            Value = self.io16list.getTimeDiff(device,interrupt_mask, port)
        else:
            Value = 0
            self.io16list.setTime(device,interrupt_mask, port)
        #print dicti
        for name in namelist:
            broadcast_input_value('TiFo.' + name, Value)
#            dicti['Name'] = 'TiFo.' + name
#            mySocket.sendto(str(dicti) ,(constants.server1,constants.broadPort))
        self.timeout_reset()

    def cb_md(self, device, uid):
#        dicti = {'Name':settings.inputs.get(uid),'Value':1}
        broadcast_input_value('TiFo.' + str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]), 1)
#        dicti = {'Name':'TiFo.' + str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]),'Value':1}
#        mySocket.sendto(str(dicti) ,(constants.server1,constants.broadPort))
        self.timeout_reset()

    def cb_md_end(self, device, uid):
#        dicti = {'Name':settings.inputs.get(uid),'Value':0}
        broadcast_input_value('TiFo.' + str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]), 0)
#        dicti = {'Name':'TiFo.' + str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]),'Value':0}
#        mySocket.sendto(str(dicti) ,(constants.server1,constants.broadPort))
        self.timeout_reset()

    def cb_si(self, value, device, uid):
        toolbox.log(device)
        time0 = time.time()
        data = []
        return
        nr_cycles = int(5 / pr.cycle_time)
        for i in range(0, nr_cycles):
            sample = device.get_intensity()
            data.append(sample)
            time.sleep(pr.cycle_time)
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        print(uhr)
        print(time.time() - time0)
        print(data)
        result = pr.analyze(data)
        print(result)
        for res in result:
            broadcast_input_value('TiFo.' + str(device.get_identity()[1]) +"."+ str(device.get_identity()[0]), res)
        self.timeout_reset()

    def set_io16_sub(self,cmd,io,value):
        port = cmd.get('Port')
        toolbox.log(cmd,io,value,port)
        if port  == 'A':
            flopmask = settings.IO16.get(io.get('addr'))[4]
            if flopmask & cmd.get('Pin') > 0:
                if value == 1:
                    normpos = settings.IO16.get(io.get('addr'))[7]
                    io.get('IO').set_port_monoflop('a', cmd.get('Pin'),((~normpos)&0b11111111),settings.IO16.get(io.get('addr'))[6])
            else:
                if value == 1:
                    mask = io.get('valueA') | cmd.get('Pin')
                else:
                    mask = io.get('valueA') & (0b11111111 & ~ cmd.get('Pin'))
                self.io16list.setValues(io.get('IO'),mask,'a')
                io.get('IO').set_port('a',mask)
        else:
            flopmask = settings.IO16.get(io.get('addr'))[5]
            if flopmask & cmd.get('Pin') > 0:
                if value == 1:
                    #working but gets overwritten but other commands
                    normpos = settings.IO16.get(io.get('addr'))[8]
                    io.get('IO').set_port_monoflop('b', cmd.get('Pin'),((~normpos)&0b11111111),settings.IO16.get(io.get('addr'))[6])
                    toolbox.log('b', cmd.get('Pin'),((~normpos)&0b11111111),settings.IO16.get(io.get('addr'))[6])
#                    mask = io.get('IO').get_port('b') | cmd.get('Pin')
#                    io.get('IO').set_port('b',mask)
#                    time.sleep(float(settings.IO16.get(io.get('addr'))[6])/1000)
#                    mask = io.get('IO').get_port('b') & (0b11111111 & ~ cmd.get('Pin'))
#                    io.get('IO').set_port('b',mask)
            else:
                if value == 1:
                    mask = io.get('IO').get_port('b') | cmd.get('Pin')
                else:
                    mask = io.get('IO').get_port('b') & (0b11111111 & ~ cmd.get('Pin'))
                self.io16list.setValues(io.get('IO'),mask,'b')
                io.get('IO').set_port('b',mask)

    def set_io16(self,device,value):
        #koennte noch auch .set_selected_values(port, selection_mask, value_mask) umgeschrieben werden
        #monoflop tut nicht
        toolbox.log(device,value)
        cmd_lsts = settings.IO16o.get(device)
        success = False
        for cmd in cmd_lsts:
            if str(cmd.get('Value')) == str(value):
                cmds = cmd.get('Commands')
                #print cmds
                if type(cmds) in (list,tuple):
                    for cmd in cmds:
                        #print cmd
                        if str(cmd.get('Value')) == '0': #erst alle auf Null setzen
                            addr = cmd.get('UID')
                            for io in self.io16list.liste:
                                if io.get('addr') == addr:
                                    self.set_io16_sub(cmd,io,cmd.get('Value'))
                                    success = True
                    for cmd in cmds:
                        if str(cmd.get('Value')) == '1': #erst alle auf Null setzen
                            addr = cmd.get('UID')
                            for io in self.io16list.liste:
                                if io.get('addr') == addr:
                                    self.set_io16_sub(cmd,io,cmd.get('Value'))
                                    success = True
                else:
                    cmd = cmds
                    addr = cmd.get('UID')
                    for io in self.io16list.liste:
                        if io.get('addr') == addr:
                            self.set_io16_sub(cmd,io,cmd.get('Value'))
                            success = True
        return success

    def _set_LED_zusammen(self, LED,start,ende,red,green,blue,transitiontime):
        laenge = (ende-start)
        o_r, o_g, o_b = LED.get('LED').get_rgb_values(start, 1)
        steps = abs(red-o_r) + abs(green-o_g) + abs(blue-o_b)
        wartezeit = float(transitiontime) / steps
        while o_r != red or o_g != green or o_b != blue:
            while (laenge) > 16:
                laenge = 16
                if (red-o_r) > 0:
                    o_r = o_r + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (red-o_r) < 0:
                    o_r = o_r - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                if (green-o_g) > 0:
                    o_g = o_g + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (green-o_g) < 0:
                    o_g = o_g - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                if (blue-o_b) > 0:
                    o_b = o_b + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (blue-o_b) < 0:
                    o_b = o_b - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                start += laenge
                laenge = (ende-start)
            else:
                if (red-o_r) > 0:
                    o_r = o_r + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (red-o_r) < 0:
                    o_r = o_r - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                if (green-o_g) > 0:
                    o_g = o_g + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (green-o_g) < 0:
                    o_g = o_g - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                if (blue-o_b) > 0:
                    o_b = o_b + 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)
                elif (blue-o_b) < 0:
                    o_b = o_b - 1
                    LED.get('LED').set_rgb_values(start, laenge, o_r, o_g, o_b)
                    time.sleep(wartezeit)


    def set_LED(self, **kwargs):
#        device, rot, gruen, blau, transitiontime, transition=ANSTEIGEND
        device = kwargs.get('Device')
#        range check kwargs
        try:
            for varia in ['red','green','blue']:
                if int(kwargs.get(varia)) > 255:
                    kwargs[varia] = 255
                if int(kwargs.get(varia)) < 0:
                    kwargs[varia] = 0
            green = int(kwargs.get('red',0))
            blue = int(kwargs.get('green',0))
            red = int(kwargs.get('blue',0))

            transitiontime = kwargs.get('transitiontime')
            transition = kwargs.get('transition',ANSTEIGEND)
            proc = kwargs.get('percentage',None)

            red_1 = kwargs.get('blue_1','None')
            green_1 = kwargs.get('red_1','None')
            blue_1 = kwargs.get('green_1','None')

            red_2 = int(kwargs.get('blue_2',0))
            green_2 = int(kwargs.get('red_2',0))
            blue_2 = int(kwargs.get('green_2',0))
        except:
            print(kwargs)
            return False
#        gradient
#        lauflicht
        LEDDict = settings.LEDsOut.get(device)
        uid = LEDDict.get('UID')
        start = LEDDict.get('Start')
        ende = LEDDict.get('Ende')
        toolbox.log(uid, start, ende)
#        TODO vectorize
        delta_r = 0
        delta_g = 0
        delta_b = 0
        if str(red_1) == 'None' and str(green_1) == 'None' and str(blue_1) == 'None':
            red = [int(red)]*16
            green = [int(green)]*16
            blue = [int(blue)]*16
            gradient = False
        else:
            laenge = (ende-start)
            if not str(red_1) == 'None':
                delta_r = int(red_1) - int(red)
                delta_pr = float(delta_r) / laenge
            else:
                delta_pr = 0
            if not str(green_1) == 'None':
                delta_g = (int(green_1) -int(green))
                delta_pg = float(delta_g) / laenge
            else:
                delta_pg = 0
            if not str(blue_1) == 'None':
                delta_b = (int(blue_1) - int(blue))
                delta_pb = float(delta_b) / laenge
            else:
                delta_pb = 0
            gradient = True

        for LED in self.LEDList.liste:
            if LED.get('addr') == uid:
                toolbox.log('Bricklet found')
                laenge = (ende-start)
                if proc != None and 0 <= proc <= 100:
                    laenge = int(float(proc)/100 * laenge)
                elif proc != None and proc < 0:
                    laenge = 0
                if (transitiontime == None or transitiontime <= 0) and not gradient:
                    while (laenge) > 16:
                        laenge = 16
#                         TODO check that command is executed
#                        while not (red, green, blue) == LED.get('LED').get_rgb_values(start, laenge):
                        LED.get('LED').set_rgb_values(start, laenge, red, green, blue)
                        start += laenge
                        laenge = (ende-start)
                    else:
                        LED.get('LED').set_rgb_values(start, laenge, red, green, blue)
                elif not (transitiontime == None or transitiontime <= 0):
#                    Ansteigend
                    if transition == ANSTEIGEND:
                        wartezeit = float(transitiontime) / (ende-start)
                        for birne in range(start,ende):
                            LED.get('LED').set_rgb_values(birne, 1, red, green, blue)
                            time.sleep(wartezeit)
                    elif transition == ABSTEIGEND:
                        wartezeit = float(transitiontime) / (ende-start)
                        for birne in list(reversed(range(start,ende))):
                            LED.get('LED').set_rgb_values(birne, 1, red, green, blue)
                            time.sleep(wartezeit)
                    elif transition == ZUSAMMEN:
                        self._set_LED_zusammen(LED,start,ende,red,green,blue,transitiontime)
                else:
                    for birne in range(start,(start+laenge)):
                        LED.get('LED').set_rgb_values(birne, 1, [int(red)]*16, [int(green)]*16, [int(blue)]*16)
                        red += delta_pr
                        green += delta_pg
                        blue += delta_pb
                    for birne in range((start+laenge),ende):
                        LED.get('LED').set_rgb_values(birne, 1, [int(red_2)]*16, [int(green_2)]*16, [int(blue_2)]*16)
#        TODO Transition, 4 types
#        von links nach rechts (ansteigend), von rechts nach links (absteigend)
#        alle zusammen, beides

        return True

    def set_drb(self, device, value):
        uid_cmds = settings.DualRelay.get(device)
        uid = ''
        for cmd in uid_cmds:
            if (cmd.get('Value')) == float(value):
                uid = cmd.get('UID')
                state = cmd.get('state')
                relaynr = cmd.get('relay')
        for relay in self.drb:
            temp_uid = str(relay.get_identity()[1]) +"."+ str(relay.get_identity()[0])
            if temp_uid == uid:
                relay.set_selected_state(relaynr, state)
                return True
        return False

    def receive_communication(self, payload, *args, **kwargs):
        toolbox.log(toolbox.kw_unpack(kwargs,'typ') == 'output', toolbox.kw_unpack(kwargs,'receiver') == 'TiFo')
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'TiFo':
            toolbox.log(payload)
            result = self.set_device(payload)
            toolbox.communication.send_message(payload, typ='return', value=result)

    def set_device(self, data_ev):
#       TODO do threaded with stop criteria
#        TODO change to send address and check if connected
        toolbox.log(data_ev)
        if settings.outputs.get(data_ev.get('Device')) == 'IO16o':
            return self.set_io16(data_ev.get('Device'),data_ev.get('Value'))
        elif settings.outputs.get(data_ev.get('Device')) == 'IO16o':
            return self.set_io16(data_ev.get('Device'),data_ev.get('Value'))
        elif settings.outputs.get(data_ev.get('Device')) == 'LEDs':
            return self.set_LED(**data_ev) #data_ev.get('Device'),data_ev.get('red'),data_ev.get('green'),data_ev.get('blue'),data_ev.get('transitiontime'))
        elif settings.outputs.get(data_ev.get('Device')) == 'DualRelay':
            return self.set_drb(data_ev.get('Device'),data_ev.get('Value'))
        else:
            return False

    def cb_enumerate(self, uid, connected_uid, position, hardware_version,
                     firmware_version, device_identifier, enumeration_type):
        #global self.led
        found = False
        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            # Enumeration for LED
            if device_identifier == LEDStrip.DEVICE_IDENTIFIER:
                self.LEDs.append(LEDStrip(uid, self.ipcon))
                temp_uid = str(self.LEDs[-1].get_identity()[1]) +"."+ str(self.LEDs[-1].get_identity()[0])
                toolbox.log('LEDStrip Bricklet', temp_uid)
                self.LEDList.addLED(self.LEDs[-1],temp_uid)
                self.LEDs[-1].set_frame_duration(200)
                if settings.LEDs.get(temp_uid) != None:
                    self.LEDs[-1].set_chip_type(settings.LEDs.get(temp_uid)[0])
                    self.LEDs[-1].set_frame_duration(settings.LEDs.get(temp_uid)[1])
                    found  = True
                toolbox.log("LEDStrip", temp_uid)
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
                if settings.IO16.get(temp_uid) != None:
                    self.io[-1].set_port_interrupt('a', settings.IO16.get(temp_uid)[0])
                    self.io[-1].set_port_interrupt('b', settings.IO16.get(temp_uid)[1])
                    self.io[-1].set_port_configuration('a', settings.IO16.get(temp_uid)[0],'i',True)
                    self.io[-1].set_port_configuration('b', settings.IO16.get(temp_uid)[1],'i',True)
                    self.io[-1].set_port_configuration('a', settings.IO16.get(temp_uid)[2],'o',False)
                    self.io[-1].set_port_configuration('b', settings.IO16.get(temp_uid)[3],'o',False)
                    #self.io[-1].set_port_monoflop('a', tifo_config.IO16.get(temp_uid)[4],0,tifo_config.IO16.get(temp_uid)[6])
                    #self.io[-1].set_port_monoflop('b', tifo_config.IO16.get(temp_uid)[5],0,tifo_config.IO16.get(temp_uid)[6])
                    self.io[-1].register_callback(self.io[-1].CALLBACK_INTERRUPT, partial( self.cb_interrupt, device = self.io[-1], uid = temp_uid ))
                    found  = True
                toolbox.log("IO16", temp_uid)

            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.al.append(AmbientLight(uid, self.ipcon))
                self.al[-1].set_illuminance_callback_threshold('o', 0, 0)
                self.al[-1].set_debounce_period(5000)
                #self.al.set_illuminance_callback_threshold('<', 30, 30)
                #self.al.set_analog_value_callback_period(10000)
                #self.al.set_illuminance_callback_period(60000)
                #self.al.register_callback(self.al.CALLBACK_ILLUMINANCE, self.cb_ambLight)
                #self.al.register_callback(self.al.CALLBACK_ILLUMINANCE_REACHED, self.cb_ambLight)
                args = self.al[-1]
                #self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, lambda event1, event2, event3, args=args: self.cb_ambLight(event1, event2, event3, args))

                self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, partial( self.cb_ambLight,  device=args))
                temp_uid = str(self.al[-1].get_identity()[1]) +"."+ str(self.al[-1].get_identity()[0])
#                thread_cb_amb = threading.Timer(60, self.thread_ambLight, [self.al[-1]])
                #t = toolbox.OwnTimer(self.delay, function=self.thread_ambLight, args = [self.al[-1]], name="Ambient Light")
                #self.threadliste.append(t)
                #t.start()
                found  = True
                toolbox.log("AmbientLight", temp_uid)


            if device_identifier == BrickletAmbientLightV2.DEVICE_IDENTIFIER:
                self.al.append(BrickletAmbientLightV2(uid, self.ipcon))
                self.al[-1].set_illuminance_callback_threshold('o', 0, 0)
                self.al[-1].set_debounce_period(5000)
                args = self.al[-1]
                self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, partial( self.cb_ambLight,  device=args))
                temp_uid = str(self.al[-1].get_identity()[1]) +"."+ str(self.al[-1].get_identity()[0])
                found  = True
                toolbox.log("AmbientLight", temp_uid)

            if device_identifier == BrickletCO2.DEVICE_IDENTIFIER:
                self.co2.append(BrickletCO2(uid, self.ipcon))
                temp_uid = str(self.co2[-1].get_identity()[1]) +"."+ str(self.co2[-1].get_identity()[0])
                self.co2[-1].set_co2_concentration_callback_period(45000)
                args = self.co2[-1]
                self.co2[-1].register_callback(self.co2[-1].CALLBACK_CO2_CONCENTRATION, partial( self.cb_value,  device=args))
#                thread_co2_ = threading.Timer(5, self.thread_CO2, [self.co2[-1]])
#                thread_co2_.start()
#                self.threadliste.append(thread_co2_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_CO2, args = [self.co2[-1]], name="CO2 Bricklet")
#                self.threadliste.append(t)
#                t.start()
                found  = True
                toolbox.log("BrickletCO2", temp_uid)


            if device_identifier == BrickletDualRelay.DEVICE_IDENTIFIER:
                self.drb.append(BrickletDualRelay(uid, self.ipcon))
                temp_uid = str(self.drb[-1].get_identity()[1]) +"."+ str(self.drb[-1].get_identity()[0])
                toolbox.log('Dual Relay Bricklet', temp_uid)
                found  = True
                toolbox.log("BrickletDualRelay", temp_uid)

#            if device_identifier == Moisture.DEVICE_IDENTIFIER:
#                self.moist = Moisture(uid, self.ipcon)
#                self.moist.set_moisture_callback_period(10000)
#                self.moist.register_callback(self.moist.CALLBACK_MOISTURE, self.cb_moisture)

            if device_identifier == BrickletMotionDetector.DEVICE_IDENTIFIER:
                self.md.append(BrickletMotionDetector(uid, self.ipcon))
                temp_uid = str(self.md[-1].get_identity()[1]) +"."+ str(self.md[-1].get_identity()[0])
                toolbox.log('Motion Detector Bricklet', temp_uid)
                self.md[-1].register_callback(self.md[-1].CALLBACK_MOTION_DETECTED, partial( self.cb_md, device = self.md[-1], uid = temp_uid ))
                self.md[-1].register_callback(self.md[-1].CALLBACK_DETECTION_CYCLE_ENDED, partial( self.cb_md_end, device = self.md[-1], uid = temp_uid ))
                found  = True
                toolbox.log("BrickletMotionDetector", temp_uid)

            if device_identifier == BrickletSoundIntensity.DEVICE_IDENTIFIER:
                self.si.append(BrickletSoundIntensity(uid, self.ipcon))
                temp_uid = str(self.si[-1].get_identity()[1]) +"."+ str(self.si[-1].get_identity()[0])
                toolbox.log('Sound Intensity Bricklet', temp_uid)
                self.si[-1].set_debounce_period(60000)
                self.si[-1].register_callback(self.si[-1].CALLBACK_INTENSITY_REACHED, partial( self.cb_si, device = self.si[-1], uid = temp_uid ))
                self.si[-1].set_intensity_callback_threshold('>',200,0)
                found  = True
                toolbox.log("BrickletSoundIntensity", temp_uid)

            if device_identifier == BrickletPTC.DEVICE_IDENTIFIER:
                self.ptc.append(BrickletPTC(uid, self.ipcon))
                temp_uid = str(self.ptc[-1].get_identity()[1]) +"."+ str(self.ptc[-1].get_identity()[0])
                self.ptc[-1].set_temperature_callback_period(45000)
                args = [self.ptc[-1], 100.0]
                self.ptc[-1].register_callback(self.ptc[-1].CALLBACK_TEMPERATURE, partial( self.cb_value,  device=self.ptc[-1], div=100.0))
#                thread_pt_ = threading.Timer(5, self.thread_pt, [self.ptc[-1]])
#                thread_pt_.start()
#                self.threadliste.append(thread_pt_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_pt, args = [self.ptc[-1]], name="PT temp Bricklet")
#                self.threadliste.append(t)
#                t.start()
                found  = True
                toolbox.log("BrickletPTC", temp_uid)

            if device_identifier == BrickletTemperature.DEVICE_IDENTIFIER:
                self.temp.append(BrickletTemperature(uid, self.ipcon))
                temp_uid = str(self.temp[-1].get_identity()[1]) +"."+ str(self.temp[-1].get_identity()[0])
                self.temp[-1].set_temperature_callback_period(45000)
                self.temp[-1].register_callback(self.temp[-1].CALLBACK_TEMPERATURE, partial( self.cb_value,  device=self.temp[-1], div=100.0))
#                thread_pt_ = threading.Timer(10, self.thread_pt, [self.temp[-1]])
#                thread_pt_.start()
#                self.threadliste.append(thread_pt_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_pt, args = [self.temp[-1]], name="Temperature Bricklet")
#                self.threadliste.append(t)
#                t.start()
                found  = True
                toolbox.log("BrickletTemperature", temp_uid)

            if device_identifier == BrickletBarometer.DEVICE_IDENTIFIER:
                self.baro.append(BrickletBarometer(uid, self.ipcon))
                temp_uid = str(self.baro[-1].get_identity()[1]) +"."+ str(self.baro[-1].get_identity()[0])
                self.baro[-1].set_air_pressure_callback_period(45000)
                self.baro[-1].register_callback(self.baro[-1].CALLBACK_AIR_PRESSURE, partial( self.cb_value,  device=self.baro[-1], div=1000.0))
#                thread_cp_ = threading.Timer(15, self.thread_cp, [self.temp[-1]])
#                thread_cp_.start()
#                self.threadliste.append(thread_cp_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_cp, args = [self.temp[-1]], name="Pressure Bricklet")
#                self.threadliste.append(t)
#                t.start()
                found  = True
                toolbox.log("BrickletBarometer", temp_uid)

            if device_identifier == BrickletHumidityV2.DEVICE_IDENTIFIER:
                self.humi.append(BrickletHumidityV2(uid, self.ipcon))
                temp_uid = str(self.humi[-1].get_identity()[1]) +"."+ str(self.humi[-1].get_identity()[0])
                self.humi[-1].set_humidity_callback_configuration(45000, False, "x", 0, 0)
                self.humi[-1].register_callback(self.humi[-1].CALLBACK_HUMIDITY, partial( self.cb_value,  device=self.humi[-1], div=100.0, ext='.HU'))
                self.humi[-1].set_temperature_callback_configuration(45000, False, "x", 0, 0)
                self.humi[-1].set_status_led_config(BrickletHumidityV2.STATUS_LED_CONFIG_OFF)
                self.humi[-1].register_callback(self.humi[-1].CALLBACK_TEMPERATURE, partial( self.cb_value,  device=self.humi[-1], div=100.0, ext='.TE'))
#                thread_hum_ = threading.Timer(20, self.thread_hum, [self.temp[-1]])
#                thread_hum_.start()
#                self.threadliste.append(thread_hum_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_hum, args = [self.temp[-1]], name="Humidity Bricklet")
#                self.threadliste.append(t)
#                t.start()
                found  = True
                toolbox.log("BrickletHumidityV2", temp_uid)

            if device_identifier == BrickletVoltageCurrent.DEVICE_IDENTIFIER:
                self.volcu.append(BrickletVoltageCurrent(uid, self.ipcon))
                temp_uid = str(self.volcu[-1].get_identity()[1]) +"."+ str(self.volcu[-1].get_identity()[0])
#                thread_volc_ = threading.Timer(25, self.thread_volc, [self.temp[-1]])
#                thread_volc_.start()
#                self.threadliste.append(thread_volc_)
#                t = toolbox.OwnTimer(self.delay, function=self.thread_volc, args = [self.temp[-1]], name="Vol Curr Bricklet")
#                self.threadliste.append(t)
#                t.start()
                self.volcu[-1].set_debounce_period(1000)
                self.volcu[-1].set_voltage_callback_period(1000)
                self.volcu[-1].set_current_callback_period(1000)
                self.volcu[-1].register_callback(self.volcu[-1].CALLBACK_VOLTAGE_REACHED, partial( self.cb_volc_vol, device = self.volcu[-1], uid = temp_uid ))
                self.volcu[-1].set_voltage_callback_threshold(">", 0, 0)
                self.volcu[-1].register_callback(self.volcu[-1].CALLBACK_CURRENT_REACHED, partial( self.cb_volc_cur, device = self.volcu[-1], uid = temp_uid ))
                self.volcu[-1].set_current_callback_threshold(">", 0, 0)
                found  = True
                toolbox.log("BrickletVoltageCurrent", temp_uid)

            if device_identifier == BrickMaster.DEVICE_IDENTIFIER:
                self.master.append(BrickMaster(uid, self.ipcon))
                temp_uid = str(self.master[-1].get_identity()[0])
                toolbox.log('Master Brick', temp_uid)
                thread_rs_error = threading.Timer(60, self.thread_RSerror, [])
                print(firmware_version)
                if firmware_version[0]*100+firmware_version[1]*10+firmware_version[2] >= 232:
                    self.master[-1].disable_status_led()
                #thread_rs_error.start()
                found  = True
                toolbox.log("BrickMaster", temp_uid)

            if not found:
                toolbox.log(connected_uid, uid, device_identifier)
                print(connected_uid, uid, device_identifier)
            else:
                self.delay += 5

    def cb_connected(self, connected_reason):
        # Enumerate devices again. If we reconnected, the Bricks/Bricklets
        # may have been offline and the configuration may be lost.
        # In this case we don't care for the reason of the connection
        while True:
            try:
                self.ipcon.enumerate()
                break
            except Error as e:
                toolbox.log('Enumerate Error: ' + str(e.description))
                time.sleep(1)


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
        while True:
            try:
                self.ipcon.enumerate()
                break
            except Error as e:
                toolbox.log('Enumerate Error: ' + str(e.description))
                time.sleep(1)



if __name__ == "__main__":
    #sb = dist_us()
    data_ev = {}
#    tf = tiFo()
#    time.sleep(2)
#    data_ev['Device'] = 'V00WOH1SRA1LI11'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#    time.sleep(2)
#    data_ev['Device'] = 'V00WOH1SRA1LI11'
#    data_ev['Value'] = 0
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V00WOH1SRA1LI01'
#    data_ev['red'] = 255
#    data_ev['green'] = 0
#    data_ev['blue'] = 0
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V00WOH1SRA1LI02'
#    data_ev['red'] = 0
#    data_ev['green'] = 255
#    data_ev['blue'] = 0
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V00WOH1SRA1LI03'
#    data_ev['red'] = 0
#    data_ev['green'] = 0
#    data_ev['blue'] = 255
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V01ZIM1RUM1DO01'
#    data_ev['Value'] = 0
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V01ZIM1RUM1DO02'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V01ZIM1RUM1DO01'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V01ZIM1RUM1DO02'
#    data_ev['Value'] = 0
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V01ZIM1RUM1DO03'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V01ZIM1RUM1DO01'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#
#    time.sleep(2)
#    data_ev['Device'] = 'V01ZIM1RUM1DO01'
#    data_ev['Value'] = 0
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V01ZIM1RUM1DO02'
#    data_ev['Value'] = 1
#    tf.set_device(data_ev)
#    data_ev['Device'] = 'V01ZIM1RUM1DO03'
#    data_ev['Value'] = 0
#    tf.set_device(data_ev)
#    raw_input('Press key to exit\n') # Use input() in Python 3
#    #sb.set_one_color(rot = 255)
    raw_input('Press key to exit\n')
    #time.sleep(15)
    #sb.flash(start = 0, new = True, n_blau = 255)
    #sb.flash(start = 15, new = True, n_blau = 255)
    #sb.flash(start = 30, new = True, n_blau = 255)
    #sb.flash(start = 30, new = True, reverse = True, n_gruen = 255)
    #sb.flash(start = 15, new = True, reverse = True, n_gruen = 255)
    #sb.flash(start = 0, new = True, reverse = True, n_gruen = 255)
    #raw_input('Press key to exit\n')
    #ipcon.disconnect()