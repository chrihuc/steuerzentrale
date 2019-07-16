# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:54:37 2019

@author: hc
"""

import datetime
import pytz

import constants
from tools import toolbox
from outputs.mqtt_publish import mqtt_pub

import pyowm

import itertools
import operator

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value)
    toolbox.communication.send_message(payload, typ='InputValue')

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


owm = pyowm.OWM(constants.owm_key, language="de")

def main():
    while constants.run:
        observation = owm.weather_at_id(2658173)
        
        forecast = owm.three_hours_forecast_at_id(2658173)
        f = forecast.get_forecast()
        lst = observation.get_weather()
        rain = 0
        if lst.get_rain():
            try:
                rain = lst.get_rain()['3h']
            except:
                pass
        winds = lst.get_wind()['speed']
        data = {'Value':rain}
        broadcast_input_value('Wetter/Regen', rain)
        data = {'Value':winds}
        broadcast_input_value('Wetter/Wind', winds)        
        jetzt = datetime.datetime.today()
        morgen = jetzt + datetime.timedelta(days=1)
        bern = pytz.timezone('Europe/Berlin')
        morgen = bern.localize(morgen)
        minimum = 100
        maximum = -100 
        stati = []   
        for weather in f:
        #    datetime.strptime(time2, format)
            if morgen >  weather.get_reference_time('date'):
                minimum = min(weather.get_temperature('celsius')['temp'], minimum)
                maximum = max(weather.get_temperature('celsius')['temp'], maximum)
                stati.append(weather.get_detailed_status())   

        w = observation.get_weather()
        value = w.get_temperature('celsius')['temp']
#        tmin = w.get_temperature('celsius')['temp_min']
#        tmax = w.get_temperature('celsius')['temp_max']
#        Status = w.get_detailed_status()
        data = {'Value':value, 'Min':minimum, 'Max':maximum, 'Status':most_common(stati), 'Regen':rain}
        mqtt_pub("Wetter/Jetzt", data)
        toolbox.sleep(60*10)
