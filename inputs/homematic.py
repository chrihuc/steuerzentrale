# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 21:50:59 2020

@author: hc
"""

import constants

import time
from pyhomematic import HMConnection



def systemcallback(src, *args):
    print(src)
    for arg in args:
        print(arg)
    
def main():
    pyhomematic = HMConnection(interface_id="myserver",
                               autostart=True,
                               systemcallback=systemcallback,
                               remotes={"rf":{
                                   "ip":"192.168.193.18",
                                   "port": 2001},
							   "ip":{
                                   "ip":"192.168.193.18",
                                   "port": 2010}})
    
if __name__ == "__main__":
    main()    