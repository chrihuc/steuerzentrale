#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 06:18:05 2019

@author: christoph
"""

from influxdb import InfluxDBClient

json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]

client = InfluxDBClient('192.168.192.2', 8086, 'customer', 'user', 'example')
client.create_database('example')
client.write_points(json_body)
result = client.query('select value from cpu_load_short;')
print("Result: {0}".format(result))