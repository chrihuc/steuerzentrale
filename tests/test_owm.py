# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:19:44 2019

@author: hc
"""

import constants

import pyowm

import datetime
import pytz
#format = '%Y-%m-%d %H:%M:%S'

import itertools
import operator

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
observation = owm.weather_at_id(2658173)
w = observation.get_weather()
if w.get_rain():
    print("raining")
print(w.get_wind()['speed'])
forecast = owm.three_hours_forecast_at_id(2658173)
f = forecast.get_forecast()
#lst = f.get_weathers()
# über  iterieren
jetzt = datetime.datetime.today()
morgen = jetzt + datetime.timedelta(days=1)
morgen = morgen.replace(hour=0, minute=0)
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
value = w.get_temperature('celsius')['temp']
tmin = w.get_temperature('celsius')['temp_min']
tmax = w.get_temperature('celsius')['temp_max']
Status = w.get_detailed_status()
data = {'Value':value, 'Min':minimum, 'Max':maximum, 'Status':most_common(stati)}

print(data)