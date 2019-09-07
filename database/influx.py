#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 06:18:05 2019

@author: christoph
"""

from influxdb import InfluxDBClient
import constants

#json_body = [
#    {
#        "measurement": "cpu_load_short",
#        "tags": {
#            "host": "server01",
#            "region": "us-west"
#        },
#        "time": "2009-11-10T23:00:00Z",
#        "fields": {
#            "value": 0.64
#        }
#    }
#]

client = InfluxDBClient(constants.sql_.IP, 8086, constants.sql_.USER, constants.sql_.PASS, 'steuerzentrale')
#client.create_database('example')
#client.write_points(json_body)
result = client.query('SELECT sum("value") FROM "A00TER1GEN1RE01" WHERE time >= now() - 7d;')
points=list(result.get_points())
print(points[0]['sum'])
#for point in points:
#    print(point['sum'])
print("Result: {0}".format(result))