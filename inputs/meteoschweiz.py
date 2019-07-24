#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import urllib.request, json 
with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-niederschlag-10min/ch.meteoschweiz.messwerte-niederschlag-10min_de.json") as url:
    data = json.loads(url.read().decode())
    for section in data:
        if section == 'features':
            for feature in data['features']:
                if feature['id'] == 'UBB':
                    print(feature['properties']['value'])
with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min_de.json") as url:
    data = json.loads(url.read().decode())
    for section in data:
        if section == 'features':
            for feature in data['features']:
                if feature['id'] == 'BUS':
                    print(feature['properties']['value'])                    
                    
with urllib.request.urlopen("https://data.geo.admin.ch/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min_de.json") as url:
    data = json.loads(url.read().decode())
    for section in data:
        if section == 'features':
            for feature in data['features']:
                if feature['id'] == 'BUS':
                    print(feature['properties']['value'])                      
#https://data.geo.admin.ch/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min/ch.meteoschweiz.messwerte-windgeschwindigkeit-kmh-10min_de.json                    
#https://data.geo.admin.ch/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min/ch.meteoschweiz.messwerte-wind-boeenspitze-kmh-10min_de.json                    