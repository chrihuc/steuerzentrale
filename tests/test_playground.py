#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:32:49 2018

@author: christoph
"""

import requests

ip = requests.get('https://api.ipify.org').text
print('My public IP address is:', ip)
