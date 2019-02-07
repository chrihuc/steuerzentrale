# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:54:37 2019

@author: hc
"""

import time

import constants
from tools import toolbox
from outputs.mqtt_publish import mqtt_pub

import pyowm

owm = pyowm.OWM(constants.owm_key, language="de")

def main():
    while constants.run:
        observation = owm.weather_at_id(2658173)
        w = observation.get_weather()
        value = w.get_temperature('celsius')['temp']
        tmin = w.get_temperature('celsius')['temp_min']
        tmax = w.get_temperature('celsius')['temp_max']
        Status = w.get_detailed_status()
        data = {'Value':value, 'Min':tmin, 'Max':tmax, 'Status':Status}
        mqtt_pub("Wetter/Jetzt", data)
        toolbox.sleep(60*10)
