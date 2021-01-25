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
from database import mysql_connector as msqc

import pyowm

import itertools
import operator
import urllib.request, json 
from influxdb import InfluxDBClient

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

def get_rain():
    with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-niederschlag-10min/ch.meteoschweiz.messwerte-niederschlag-10min_de.json") as url:
        data = json.loads(url.read().decode())
        rain, rain1, rain2 = 0,0,0
        for section in data:
            if section == 'features':
                for feature in data['features']:
                    if feature['properties']['station_name'] == 'Bözberg':
                        rain = feature['properties']['value']
                    if feature['properties']['station_name'] == 'Buchs / Aarau':
                        rain1 = feature['properties']['value']
                    if feature['properties']['station_name'] == 'Stetten':
                        rain2 = feature['properties']['value']
        return rain, rain1, rain2

def get_wind():
    with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min_de.json") as url:
        data = json.loads(url.read().decode())
        for section in data:
            if section == 'features':
                for feature in data['features']:
                    if feature['id'] == 'BUS':
                        return feature['properties']['value']
                        
def get_boeen():
    with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min_de.json") as url:
        data = json.loads(url.read().decode())
        boee1, boee2 = 0, 0
        for section in data:
            if section == 'features':
                for feature in data['features']:
                    if feature['id'] == 'BUS':
                        boee1 = feature['properties']['value']
                    if feature['id'] == 'PSI':
                        boee2 = feature['properties']['value']                        
        return boee1, boee2

def main():
    while constants.run:
        retries = 0
        while retries < 3:        
            try:
                rain, rain1, rain2 = get_rain()
                broadcast_input_value('Wetter/RegenBOZ', rain)
                broadcast_input_value('Wetter/Regen', (rain + rain1 + rain2)/3)
                #print("Wetter Regen: ", max(rain, rain1, rain2))
                broadcast_input_value('Wetter/RegenWarnung', max(rain, rain1, rain2))
                retries = 3
            except Exception as e:
                print(e)
                retries += 1                
#                print("Regen Failed")   
        retries = 0
        while retries < 3:            
            try:            
                winds = get_wind()
                broadcast_input_value('Wetter/Wind', winds) 
                retries = 3
            except Exception as e:
                print(e)
                retries += 1
#                print("Wind Failed") 
        retries = 0
        while retries < 3:             
            try:            
                boee1, boee2 = get_boeen()
                broadcast_input_value('Wetter/Boeen', max(boee1,boee2))   
                retries = 3
            except Exception as e:
                print(e)
                retries += 1
#                print("Wind Boeen Failed")              
        
        client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
        regentage = msqc.setting_r('minDohneRasenS') # 7
#        print(regentage)
        if str(regentage) != 'None':
            result = client.query('SELECT sum("value") FROM "A00TER1GEN1RE01" WHERE time >= now() - ' + str(int(float(regentage))) + 'd;')
            points=list(result.get_points())
            if points:
                broadcast_input_value('Wetter/Regen7d', points[0]['sum']/10)
            else:
                broadcast_input_value('Wetter/Regen7d', 0)
        
        retries = 0
        while retries < 3:
            try:
                observation = owm.weather_at_id(2658173)
                forecast = owm.three_hours_forecast_at_id(2658173)
                f = forecast.get_forecast()        
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
                broadcast_input_value('Internal.OWM', 1)
                retries = 3
            except:
#                print("OWM Failed")
                retries += 1
                pass
        toolbox.sleep(60*1)
