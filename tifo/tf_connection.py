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
from tinkerforge.bricklet_led_strip_v2 import BrickletLEDStripV2
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
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_barometer import BrickletBarometer
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2
from tinkerforge.bricklet_line import BrickletLine
from tinkerforge.bricklet_multi_touch import BrickletMultiTouch
from tinkerforge.bricklet_air_quality import BrickletAirQuality
from tinkerforge.brick_master import BrickMaster
from tinkerforge.ip_connection import Error

import threading
import json
#from threading import Timer
import time
from time import localtime,strftime
from math import log
import datetime
import uuid

from influxdb import InfluxDBClient

#from distutils.version import LooseVersion

import constants

# on server:
from tifo import settings
from tifo import pattern_reco as pr
from tools import toolbox
from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))



def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value, level=9)
    toolbox.communication.send_message(payload, typ='InputValue')

#    on satellite:
#    mySocket.sendto(str(payload) ,(constants.server1,constants.broadPort))

# tranisiton modes
    
def writeInfluxDb(hks, value, utc):
    try:
        if float(value) == 0:
             json_body = [{"measurement": hks,
                          "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                          "fields": {"value": 0.}}] 
        else:      
            json_body = [{"measurement": hks,
                          "time": utc,#.strftime('%Y-%m-%dT%H:%M:%SZ'), #"2009-11-10T23:00:00Z",
                          "fields": {"value": float(value)}}]
        client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
        client.write_points(json_body)
    except:
        print(hks, value, utc)
    return True    
    
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
            times.append(datetime.datetime.now() - datetime.timedelta(minutes=1))
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

class LineBrick:
    def __init__(self, device, uid):
        self.device = device
        self.uid = uid
        self.state = 0
        self.gwl = 3000
        self.gwh = 3400
        self.min = 9999
        self.max = 0
        self.counter = 0
        self.f_value = 60
        self.hour = 3600
        self.day = 3600 * 24
        self.value = 0
        self.value_h = 0
        self.value_d = 0
        self.pulsTime = datetime.datetime.now()
        self.name = str(self.device.get_identity()[1]) +"."+ str(self.device.get_identity()[0])
        lt = localtime()
        sekunde = int(strftime("%S", lt))    
        minute = int(strftime("%M", lt)) 
        stunde = int(strftime("%H", lt))  
        self.load()
        self.readout = threading.Timer(self.f_value - sekunde, self.evaluate)
        self.readout.start()
        self.readout_h = threading.Timer(self.hour - (minute * 60) - sekunde, self.evaluate_h)
        self.readout_h.start()
        self.readout_d = threading.Timer(self.day - (stunde * 3600) - (minute * 60) - sekunde, self.evaluate_d)
        self.readout_d.start()       
        self.reset = threading.Timer(60, self.reset_delta)         
        toolbox.log('line Bricklet created', level=5)
     
    def reset_delta(self):
        #self.pulsTime = datetime.datetime.now()
        broadcast_input_value('TiFo.' + self.name + '.raw', str(0))
        
    def callback(self, value):
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        if value < self.gwl and self.state == 1:
            self.state = 0
            delta = datetime.datetime.now() - self.pulsTime
            self.pulsTime = datetime.datetime.now()
            if delta.total_seconds() > 0: 
                broadcast_input_value('TiFo.' + self.name + '.raw', str(20/delta.total_seconds()))
            self.reset.cancel()
            self.reset = threading.Timer(2*delta.total_seconds(), self.reset_delta)
            self.reset.start()            
        elif value < self.gwl:
            self.state = 0
        if value > self.gwh and self.state == 0:
            self.state = 1
            delta = datetime.datetime.now() - self.pulsTime
            self.pulsTime = datetime.datetime.now()
            if delta.total_seconds() > 0: 
                broadcast_input_value('TiFo.' + self.name + '.raw', str(40/delta.total_seconds()))
            self.reset.cancel()
            self.reset = threading.Timer(2*delta.total_seconds(), self.reset_delta)
            self.reset.start()              
            self.counter += 1
            self.value_h += 1
            self.value_d += 1
            self.store()
        
    def evaluate(self):
        self.value = self.counter / 60 * self.f_value
        self.counter = 0
        toolbox.log('min reset', level=5)
        broadcast_input_value('TiFo.' + self.name + '.minute', str(self.value))
        self.store()
        self.readout = threading.Timer(self.f_value, self.evaluate)
        self.readout.start()
     
    def evaluate_h(self):
        broadcast_input_value('TiFo.' + self.name + '.hour', str(self.value_h))
        self.value_h = 0    
        self.readout_h = threading.Timer(self.hour, self.evaluate_h)
        self.readout_h.start()
        
    def evaluate_d(self):
        broadcast_input_value('TiFo.' + self.name + '.day', str(self.value_d))
        broadcast_input_value('TiFo.' + self.name + '.minimum', str(self.min))
        broadcast_input_value('TiFo.' + self.name + '.maximum', str(self.max))
        if self.min > 0 and (self.max - self.min) > 600:
            self.gwl = self.min + 200
            self.gwh = self.max - 200
        self.value_d = 0   
        self.min = 9999
        self.max = 0     
        self.readout_d = threading.Timer(self.day, self.evaluate_d)
        self.readout_d.start()           
        
    def stop_timers(self):
        self.readout.cancel()
        self.readout_h.cancel()
        self.readout_d.cancel()
        
    def store(self):
        write_list = {'self.counter' : self.counter,
                      'self.state'     : self.state,                      
                      'self.value_h' : self.value_h,
                      'self.value_d' : self.value_d,
                      'self.min'     : self.min,
                      'self.max'     : self.max,
                      'self.gwl'     : self.gwl,
                      'self.gwh'     : self.gwh}
        with open(self.uid + '.jsn', 'w') as fout:
            json.dump(write_list, fout, default=json_serial)    

    def load(self):
        try:
#        if True:
            with open(self.uid + '.jsn') as f:
                full = f.read()            
            alte = json.loads(full)
            self.counter = alte['self.counter']
            self.state = alte['self.state']            
            self.value_h = alte['self.value_h']
            self.value_d = alte['self.value_d']
            self.min = alte['self.min']
            self.max = alte['self.max']
            self.gwl = alte['self.gwl']
            self.gwh = alte['self.gwh']
        except:
            toolbox.log('Laden der Wasserzaehler Impulse fehlgeschlagen', level=1)

class LEDStrips:
    def __init__(self):
        self.liste = []
        self.keys = []

    def addLED(self, LED,addr,typ=1):
        global liste
        dicti = {}
        dicti["LED"] = LED
        dicti['addr'] = addr
        dicti['typ'] = typ
        dicti['busy'] = False
        dicti['stop'] = False
        self.keys.append(addr)
        self.liste.append(dicti)

class MT_Bricklet:
    def __init__(self, device, uid):
        self.device = device
        self.uid = uid
        self.state  = 0
        self.times = {(1 << bit):datetime.datetime.now() for bit in range(12, -1, -1)}
        
    def get_time(self, name, value):
        secs = 0
        if value == 1:
            self.times[name] = datetime.datetime.now()
        elif value == 0:
            if name in self.times:
                timedelta = datetime.datetime.now() - self.times[name]
                secs = timedelta.total_seconds()
        return secs
        
    def event_happened(self, param):
        change = self.state ^ param
        changes = {}
        bit_list = [(1 << bit) for bit in range(12, -1, -1)]
        for wert in bit_list:
            if change & wert > 0:
                name = self.uid + "." + str(bin(wert))
                if name != None:
                    value = wert & param
                    result = self.get_time(name, value)
                    changes[name] = result       
        self.state = param
        return changes

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
        toolbox.log('TiFo init start')
        self.led = None
        self.io = []
        self.io16list = io16Dict()
        self.LEDs = []
        self.LEDList = LEDStrips()
        self.al = []
        self.drb = []
        self.drbuids = {}
        self.master = []
        self.md = []
        self.si = []
        self.ptc = []
        self.temp = []
        self.baro = []
        self.humi = []
        self.co2 = []
        self.volcu = []
        self.aiq = []
        self.moist = None
        self.unknown = []
        self.threadliste = []
        self.lineBricklets = {}
        self.multitouchBricklets = {}
        self.dus = []
        self.ip = ip
        self.delay = 5
        self.timeoutTime = 300
        self.timeout = threading.Timer(self.timeoutTime, self.timedOut)

        self.ipcon = IPConnection()
        self.ipcon.set_timeout(10)
        
        self.command_queue = {}

        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE,
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED,
                                     self.cb_connected)
        toolbox.log('TiFo init done')
  


    def timeout_reset(self):
        self.timeout.cancel()
        self.timeout = threading.Timer(self.timeoutTime, self.timedOut)
        self.timeout.start()

    def timedOut(self):
        aes.new_event(description="Tifo timedOut: "+self.ip, prio=9)
        self.connect()

    def connect(self):
        try:
            self.ipcon.disconnect()
#            print('disconnected: ' + self.ip)
        except:
            pass
        # Connect to brickd, will trigger cb_connected
        while True:
            try:
#                print('connecting to: ' + self.ip)
                self.ipcon.connect(self.ip, PORT)
#                aes.new_event(description="Tifo connected: "+self.ip, prio=9)
                break
            except Error as e:
                print('Connection Error: ' + str(e.description))
                time.sleep(10)
            except socket.error as e:
#                print('Socket error: ' + str(e))
                time.sleep(10)
        toolbox.communication.register_callback(self.receive_communication)
        time.sleep(5)
        toolbox.log('TiFo started')

    def main(self):
        # Create IP Connection
        self.connect()
        while constants.run and not constants.test:
            toolbox.sleep(3)
        if not constants.test:
            self.disconnect()

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


    def disconnect(self):
        self.ipcon.disconnect()
        print('disconnected: ' + self.ip)

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

    def cb_values(self, value, accuracy,device,div=1.0,ext='',uid=''):
        toolbox.log(device)
#        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + uid + ext, str(value/div))
        self.timeout_reset()

    def cb_aiq_values(self, *args, **kwargs):
#        print(args)
#        print(kwargs)
#        toolbox.log(device)
        broadcast_input_value('TiFo.' + kwargs['uid'] + '.aiq', str(args[0]/1.0))
        broadcast_input_value('TiFo.' + kwargs['uid'] + '.acc', str(args[1]/1.0))
        broadcast_input_value('TiFo.' + kwargs['uid'] + '.temp', str(args[2]/100.0))
        broadcast_input_value('TiFo.' + kwargs['uid'] + '.hum', str(args[3]/100.0))
        broadcast_input_value('TiFo.' + kwargs['uid'] + '.pres', str(args[4]/100.0))
        self.timeout_reset()

    def cb_value_uid(self, value,device,div=1.0,ext='',uid=''):
        toolbox.log(device)
        name = uid
        broadcast_input_value('TiFo.' + name + ext, str(value/div))
        self.timeout_reset()

    def cb_dist_value(self, value,device,div=1.0,ext='', threshold=20, name='none.none'):
        toolbox.log(device)
#        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name + ext, str(value/div))
        device.set_distance_callback_threshold('o', value-threshold, value+threshold)
        self.timeout_reset()        

    def thread_ambLight(self, device):
        while constants.run:
#            toolbox.log(device)
            try:
                illuminance = device.get_illuminance()
                name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
                broadcast_input_value('TiFo.' + name, str(illuminance))
            except:
                pass                
            toolbox.sleep(60)

    def thread_CO2(self, device):
        while constants.run:
            toolbox.log(device)
            value = device.get_co2_concentration()
            name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
            broadcast_input_value('TiFo.' + name, str(value))
            toolbox.sleep(60)

    def thread_distus(self, device):
        counter = 0
        while constants.run:
            try:
                value = device.get_distance_value()
                name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
                broadcast_input_value('TiFo.' + name, str(value))
                counter = 0
            except:
                counter += 1
                if counter > 20:
                    self.timedOut()
                    break
            toolbox.sleep(0.5)

    def thread_pt(self, device):
        while constants.run:
            try:
                value = device.get_temperature()
                name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
                broadcast_input_value('TiFo.' + name, str(float(value)/100))
                self.timeout_reset()
            except:
                pass                
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
            try:
                value = device.get_humidity()
                name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
                broadcast_input_value('TiFo.' + name + '.HU', str(float(value)/100))
                toolbox.sleep(10)
                value = device.get_temperature()
                broadcast_input_value('TiFo.' + name + '.TE', str(float(value)/100))
            except:
                pass                 
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
        if value < 2500:
            broadcast_input_value('TiFo.' + name + '.Riegel', str(1))
        else:
            broadcast_input_value('TiFo.' + name + '.Riegel', str(0))
        broadcast_input_value('TiFo.' + name + '.U', str(float(value)/1000))
        self.timeout_reset()

    def cb_volc_cur(self, value, device, uid):
        toolbox.log(device)
        name = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
        broadcast_input_value('TiFo.' + name + '.I', str(float(value)/100))
        self.timeout_reset()
        
    def thread_io16(self, device, uid):
        while constants.run:
            ports = ['a','b']
            for port in ports:
                result = device.get_port(port)
                for i in range(0,7):
                    mask = 1 << i
                    try:
                        self.cb_interrupt(port,mask,result,device,uid,thread=True)
                    except Exception as e:
                        print(e)
            time.sleep(30)

    def cb_interrupt(self, port, interrupt_mask, value_mask, device, uid, thread=False):
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
            #if Value == 0: # nach dem neustart ist das 0
            #   Value = 1
        else:
            Value = 0
            if not thread:
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
#        return
        nr_cycles = int(5 / pr.cycle_time)
        for i in range(0, nr_cycles):
#           ToDo: handle timeouts here
            sample = device.get_intensity()
            data.append(sample)
            time.sleep(pr.cycle_time)
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
#        print(uhr)
#        print(time.time() - time0)
#        print(data)
        result = pr.analyze(data)
#        print(result)
        for res in result:
            broadcast_input_value('TiFo.' + uid, res)
        self.timeout_reset()

    def cb_li(self, value, device, uid):
#        temp_uid = str(device.get_identity()[1]) +"."+ str(device.get_identity()[0])
#        print(value)
        self.lineBricklets[uid].callback(value)
#        utc = datetime.datetime.utcnow()
#        writeInfluxDb(temp_uid, value, utc)

    def cb_mtb(self, param, uid):
        changes = self.multitouchBricklets[uid].event_happened(param)
        for key, value in changes.items():
            broadcast_input_value('TiFo.' + key, value)

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
#                                    broadcast_input_value('TiFo.' + temp_uid, str(value))
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


    def set_LED(self, adress, **kwargs):
#        device, rot, gruen, blau, transitiontime, transition=ANSTEIGEND
        device = kwargs.get('Device')
        self.command_queue[adress] = kwargs 
        try:
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
    #        LEDDict = settings.LEDsOut.get(device)
    #        uid = LEDDict.get('UID')
    #        start = LEDDict.get('Start')
    #        ende = LEDDict.get('Ende')
            if transitiontime:
                transitiontime = int(str(transitiontime))
            
            uid = adress.split(".")[1] + '.' + adress.split(".")[2]
            if toolbox.kw_unpack(kwargs, 'start'):
                start = int(str(toolbox.kw_unpack(kwargs, 'start')))
            else:
                start = int(adress.split(".")[3])
            if toolbox.kw_unpack(kwargs, 'ende'):
                ende = int(str(toolbox.kw_unpack(kwargs, 'ende')))
            else:
                ende = int(adress.split(".")[4])  
            
            toolbox.log(uid, start, ende)
    #        TODO vectorize
            delta_r = 0
            delta_g = 0
            delta_b = 0
            red_i = red
            green_i = green
            blue_i = blue
            if str(red_1) == 'None' and str(green_1) == 'None' and str(blue_1) == 'None':
                red = [int(red)]*16
                green = [int(green)]*16
                blue = [int(blue)]*16
                gradient = False
            else:
                laenge = (ende-start)
                red_1 = int(red_1)
                green_1 = int(green_1)
                blue_1 = int(blue_1)
                if not str(red_1) == 'None':
                    delta_r = abs(int(red_1) - int(red))
                    delta_pr = float(delta_r) / laenge
                else:
                    delta_pr = 0
                if not str(green_1) == 'None':
                    delta_g = abs(int(green_1) -int(green))
                    delta_pg = float(delta_g) / laenge
                else:
                    delta_pg = 0
                if not str(blue_1) == 'None':
                    delta_b = abs(int(blue_1) - int(blue))
                    delta_pb = float(delta_b) / laenge
                else:
                    delta_pb = 0
                gradient = True
                steps = (delta_r + delta_g + delta_b) * laenge
    
    
            for LED in self.LEDList.liste:
                if LED.get('addr') == uid:
                    while LED['busy']:
                        LED['stop'] = True
                        time.sleep(0.1)
                    LED['stop'] = False
                    typ = LED['typ']
                    batch = 16
                    if typ == 2:
                        batch = 2048
                    toolbox.log('Bricklet found')
                    laenge = (ende-start)
                    if proc != None and 0 <= proc <= 100:
                        laenge = int(float(proc)/100 * laenge)
                    elif proc != None and proc < 0:
                        laenge = 0
                    if (transitiontime == None or transitiontime <= 0) and not gradient:
                        while (laenge) > batch:
                            laenge = batch
    #                         TODO check that command is executed
    #                        while not (red, green, blue) == LED.get('LED').get_rgb_values(start, laenge):
                            if typ == 1:
                                LED.get('LED').set_rgb_values(start, laenge, red, green, blue)
                            else:
                                rgb = [red_i,green_i,blue_i]*laenge
                                LED.get('LED').set_led_values(start*3,rgb)
                            start += laenge
                            laenge = (ende-start)
                        else:
                            if typ == 1:
                                LED.get('LED').set_rgb_values(start, laenge, red, green, blue)
                            else:
                                LED.get('LED').set_led_values(start*3,[red_i,green_i,blue_i]*laenge)
                    elif not (transitiontime == None or transitiontime <= 0):
    #                    Ansteigend licht für licht direkt zur farbe
                        wartezeit = float(transitiontime) / steps
                        LED['busy'] = True
                        while ( (red_1-red)!=0 or (green_1-green)!=0 or (blue_1-blue)!=0 ) and typ!=1 and not LED['stop']:
                            if (red_1-red)!=0:
                                if red_1 > red:
                                    red_1 -= 1
                                else:
                                    red_1 += 1
                                for birne in range(start,ende):
                                    LED.get('LED').set_led_values(birne*3,[red_1,green_1,blue_1]*1)
                                    time.sleep(wartezeit)
                            if (green_1-green)!=0:
                                if green_1 > green:
                                    green_1 -= 1
                                else:
                                    green_1 += 1
                                for birne in range(start,ende):
                                    LED.get('LED').set_led_values(birne*3,[red_1,green_1,blue_1]*1)
                                    time.sleep(wartezeit)
                            if (blue_1-blue)!=0:
                                if blue_1 > blue:
                                    blue_1 -= 1
                                else:
                                    blue_1 += 1
                                for birne in range(start,ende):
                                    LED.get('LED').set_led_values(birne*3,[red_1,green_1,blue_1]*1)
                                    time.sleep(wartezeit)                               
                        LED['busy'] = False
    #                    if transition == ANSTEIGEND:
    #                        wartezeit = float(transitiontime) / (ende-start)
    #                        for birne in range(start,ende):
    #                            if typ == 1:
    #                                LED.get('LED').set_rgb_values(birne, 1, red, green, blue)
    #                            else:
    #                                print(birne,[red_i,green_i,blue_i]*1)
    #                                LED.get('LED').set_led_values(birne*3,[red_i,green_i,blue_i]*1)
    #                            time.sleep(wartezeit)
    #                    elif transition == ABSTEIGEND:
    #                        wartezeit = float(transitiontime) / (ende-start)
    #                        for birne in list(reversed(range(start,ende))):
    #                            if typ == 1:
    #                                LED.get('LED').set_rgb_values(birne, 1, red, green, blue)
    #                            else:
    #                                LED.get('LED').set_led_values(birne*3,[red_i,green_i,blue_i]*1)
    #                            time.sleep(wartezeit)
    #                    elif transition == ZUSAMMEN:
    #                        self._set_LED_zusammen(LED,start,ende,red,green,blue,transitiontime)
                            
                    else:   # also mit gradient
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
            self.command_queue[adress] = None
        except:
            print("konnte tfled nicht ausführen")
        return True

    def set_drb(self, device, value, adress):
        temp_uid = adress.split('.')[1] + '.' + adress.split('.')[2]
        relaynr = int(adress.split('.')[3])
        relay = self.drbuids[temp_uid]
        state = bool(int(value))
        relay.set_selected_state(relaynr, state)
        broadcast_input_value('TiFo.' + temp_uid + '.' + str(relaynr), str(value))
#        for cmd in uid_cmds:
#            if (cmd.get('Value')) == float(value):
#                uid = cmd.get('UID')
#                state = cmd.get('state')
#                relaynr = cmd.get('relay')
#        for relay in self.drb:
#            temp_uid = str(relay.get_identity()[1]) +"."+ str(relay.get_identity()[0])
#            if temp_uid == uid:
#                relay.set_selected_state(relaynr, state)
        return True


    def receive_communication(self, payload, *args, **kwargs):
        toolbox.log(toolbox.kw_unpack(kwargs,'typ') == 'output', toolbox.kw_unpack(kwargs,'receiver') == 'TiFo')
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'TiFo':
            toolbox.log(payload)
            result = self.set_device(payload, adress=toolbox.kw_unpack(kwargs,'adress'))
            toolbox.communication.send_message(payload, typ='return', value=result)

    def set_device(self, data_ev, adress=None):
#       TODO do threaded with stop criteria
#        TODO change to send address and check if connected
        try:
            toolbox.log(data_ev)
            uid = adress.split(".")[1] + '.' + adress.split(".")[2]
            if settings.outputs.get(data_ev.get('Device')) == 'IO16o':
                return self.set_io16(data_ev.get('Device'),data_ev.get('Value'))
            elif settings.outputs.get(data_ev.get('Device')) == 'IO16o':
                return self.set_io16(data_ev.get('Device'),data_ev.get('Value'))
#            elif settings.outputs.get(data_ev.get('Device')) == 'LEDs':
            elif uid in self.LEDList.keys:
                return self.set_LED(adress, **data_ev) #data_ev.get('Device'),data_ev.get('red'),data_ev.get('green'),data_ev.get('blue'),data_ev.get('transitiontime'))
    #        elif settings.outputs.get(data_ev.get('Device')) == 'DualRelay':
            elif uid in self.drbuids.keys():
    #            print(data_ev.get('Device'), adress, data_ev.get('Value'), adress)
                return self.set_drb(data_ev.get('Device'),data_ev.get('Value'), adress)
            else:
                return False
        except Error as e:
            print(e)

    def cb_enumerate(self, uid, connected_uid, position, hardware_version,
                     firmware_version, device_identifier, enumeration_type):
        #global self.led
        found = False
        while True:
            try:
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
        
                    if device_identifier == BrickletLEDStripV2.DEVICE_IDENTIFIER:
                        self.LEDs.append(BrickletLEDStripV2(uid, self.ipcon))
                        temp_uid = str(self.LEDs[-1].get_identity()[1]) +"."+ str(self.LEDs[-1].get_identity()[0])
                        toolbox.log('LEDStrip Bricklet', temp_uid)
                        self.LEDList.addLED(self.LEDs[-1],temp_uid, typ=2)
                        self.LEDs[-1].set_frame_duration(200)
                        self.LEDs[-1].set_chip_type(2812)
                        found  = True
                        self.LEDs[-1].set_status_led_config(0)
                        toolbox.log("LEDStrip", temp_uid)
        
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
                            thread_io_ = threading.Timer(0, self.thread_io16, [self.io[-1],temp_uid])
                            thread_io_.start()                                 
                            found  = True
                        toolbox.log("IO16", temp_uid)
        
                    if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                        self.al.append(AmbientLight(uid, self.ipcon))
                        self.al[-1].set_illuminance_callback_threshold('o', 0, 0)
                        self.al[-1].set_debounce_period(5000)
                        #self.al.set_illuminance_callback_threshold('<', 30, 30)
                        #self.al.set_analog_value_callback_period(10000)
                        self.al[-1].set_illuminance_callback_period(5000)
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
        
                        thread_pt_ = threading.Timer(30, self.thread_ambLight, [self.al[-1]])
                        thread_pt_.start()                
                        
                        found  = True
                        toolbox.log("AmbientLight", temp_uid)
        
        
                    if device_identifier == BrickletAmbientLightV2.DEVICE_IDENTIFIER:
                        self.al.append(BrickletAmbientLightV2(uid, self.ipcon))
                        self.al[-1].set_illuminance_callback_threshold('o', 0, 0)
                        self.al[-1].set_debounce_period(5000)
                        self.al[-1].set_illuminance_callback_period(5000)
                        args = self.al[-1]
                        self.al[-1].register_callback(self.al[-1].CALLBACK_ILLUMINANCE_REACHED, partial( self.cb_ambLight,  device=args))
                        temp_uid = str(self.al[-1].get_identity()[1]) +"."+ str(self.al[-1].get_identity()[0])
                        thread_pt_ = threading.Timer(40, self.thread_ambLight, [self.al[-1]])
                        thread_pt_.start()                  
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
                        self.drbuids[temp_uid] = BrickletDualRelay(uid, self.ipcon)
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
        
                    if device_identifier == BrickletPTCV2.DEVICE_IDENTIFIER:
                        tptc = BrickletPTCV2(uid, self.ipcon)
                        self.ptc.append(tptc)
                        temp_uid = str(self.ptc[-1].get_identity()[1]) +"."+ str(self.ptc[-1].get_identity()[0])
                        tptc.set_temperature_callback_configuration(45000, False, 'o', 0, 0)
                        tptc.set_wire_mode(4)
#                        args = [self.ptc[-1], 100.0]
                        self.ptc[-1].register_callback(self.ptc[-1].CALLBACK_TEMPERATURE, partial( self.cb_value_uid,  device=self.ptc[-1], div=100.0, uid=temp_uid))
                        found  = True
                        toolbox.log("BrickletPTC", temp_uid)
        
                    if device_identifier == BrickletTemperature.DEVICE_IDENTIFIER:
                        self.temp.append(BrickletTemperature(uid, self.ipcon))
                        temp_uid = str(self.temp[-1].get_identity()[1]) +"."+ str(self.temp[-1].get_identity()[0])
                        self.temp[-1].set_temperature_callback_period(45000)
                        self.temp[-1].register_callback(self.temp[-1].CALLBACK_TEMPERATURE, partial( self.cb_value,  device=self.temp[-1], div=100.0))
                        thread_pt_ = threading.Timer(10, self.thread_pt, [self.temp[-1]])
                        thread_pt_.start()
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
                        thread_hum_ = threading.Timer(20, self.thread_hum, [self.humi[-1]])
                        thread_hum_.start()
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
        
                    if device_identifier == BrickletLine.DEVICE_IDENTIFIER:
                        lb = BrickletLine(uid, self.ipcon)
                        temp_uid = str(lb.get_identity()[1]) +"."+ str(lb.get_identity()[0])
                        if not temp_uid in self.lineBricklets:
                            self.lineBricklets[temp_uid] = LineBrick(lb, uid)
                        lb.register_callback(lb.CALLBACK_REFLECTIVITY_REACHED, partial( self.cb_li, device = lb, uid = temp_uid ))
                        lb.set_debounce_period(500)
                        lb.set_reflectivity_callback_threshold('o', 3649, 3650)
                        toolbox.log('Line Bricklet', temp_uid)
                        found  = True
        
                    if device_identifier == BrickletDistanceUS.DEVICE_IDENTIFIER:
                        self.dus.append(BrickletDistanceUS(uid, self.ipcon))
                        temp_uid = str(self.dus[-1].get_identity()[1]) +"."+ str(self.dus[-1].get_identity()[0])
        #                self.dus[-1].register_callback(self.dus[-1].CALLBACK_DISTANCE, partial( self.cb_value_uid, device = self.dus[-1], uid = temp_uid))
        #                self.dus[-1].set_distance_callback_threshold('o', 0, 0)
                        self.dus[-1].set_moving_average(100)
        #                self.dus[-1].register_callback(self.dus[-1].CALLBACK_DISTANCE_REACHED, partial( self.cb_dist_value, device = self.dus[-1]))
        #                self.dus[-1].set_distance_callback_period(5000)
                        
                        thread_us_ = threading.Timer(10, self.thread_distus, [self.dus[-1]])
                        thread_us_.start()                
                        
                        toolbox.log("BrickletDistanceUS", temp_uid)
                        found  = True
        
                    if device_identifier == BrickletMultiTouch.DEVICE_IDENTIFIER:
                        mtb = BrickletMultiTouch(uid, self.ipcon)
                        temp_uid = str(mtb.get_identity()[1]) +"."+ str(mtb.get_identity()[0])
                        if not temp_uid in self.multitouchBricklets:
                            self.multitouchBricklets[temp_uid] = MT_Bricklet(mtb, uid)
                        mtb.register_callback(mtb.CALLBACK_TOUCH_STATE, partial( self.cb_mtb, uid = temp_uid))
                        mtb.set_electrode_sensitivity(130)
                        mtb.recalibrate()
                        toolbox.log('Multitouch Bricklet', temp_uid)
                        found  = True
        
                    if device_identifier == BrickletAirQuality.DEVICE_IDENTIFIER:
                        aiq = BrickletAirQuality(uid, self.ipcon)
                        self.aiq.append(BrickletAirQuality(uid, self.ipcon))
                        temp_uid = str(self.aiq[-1].get_identity()[1]) +"."+ str(self.aiq[-1].get_identity()[0])
                        aiq.set_status_led_config(0)
#                        aiq.set_iaq_index_callback_configuration(45000, False)
#                        aiq.set_humidity_callback_configuration(45000, False, 'o', 0, 0)
#                        aiq.set_air_pressure_callback_configuration(45000, False, 'o', 0, 0)
#                        aiq.set_temperature_callback_configuration(45000, False, 'o', 0, 0)
#                        aiq.register_callback(aiq.CALLBACK_IAQ_INDEX, partial( self.cb_values,  device=aiq, div=1.0, ext=".aiq", uid=temp_uid))
#                        aiq.register_callback(aiq.CALLBACK_TEMPERATURE, partial( self.cb_value,  device=aiq, div=100.0, ext=".temp", uid=temp_uid))
#                        aiq.register_callback(aiq.CALLBACK_HUMIDITY, partial( self.cb_value,  device=aiq, div=100.0, ext=".hum", uid=temp_uid))
#                        aiq.register_callback(aiq.CALLBACK_AIR_PRESSURE, partial( self.cb_value,  device=aiq, div=100.0, ext=".pres", uid=temp_uid))
                        
                        self.aiq[-1].set_all_values_callback_configuration(45000, False)
                        self.aiq[-1].register_callback(self.aiq[-1].CALLBACK_ALL_VALUES, partial( self.cb_aiq_values,  device=aiq, uid=temp_uid))
                        found  = True
                        toolbox.log("BrickletAIQ", temp_uid)        
        
                    if device_identifier == BrickMaster.DEVICE_IDENTIFIER:
                        self.master.append(BrickMaster(uid, self.ipcon))
                        temp_uid = str(self.master[-1].get_identity()[0])
                        thread_rs_error = threading.Timer(60, self.thread_RSerror, [])
        #                print(firmware_version)
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
                break
            except Error as e:
                toolbox.log('Enumerate Error: ' + str(e.description))
                time.sleep(10)                        

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
                time.sleep(10)


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
