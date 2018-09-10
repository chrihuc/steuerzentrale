#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: christoph
"""


import threading
import time

from tools.toolbox import OwnTimer
        
     
        
threadliste = []


def a1():
    print 'a1 started'
    while True:
        time.sleep(10)
        print 'a1 running'         

def b2():
    print 'b2 started'
    time.sleep(10)   
    print 'b2 stopping'

#t = threading.Thread(name="a1", target=a1, args = [])
t = OwnTimer(0, function=a1, args = [], name="a1")
threadliste.append(t)
t.start()

#t = threading.Thread(name="b2", target=b2, args = [])
t = OwnTimer(0, function=b2, args = [], name="b2")
threadliste.append(t)
t.start()

#print dir(t)

while True:
    for t in threadliste:
        if not t in threading.enumerate():
                print t.name, ' stopped'
#                new_t = threading.Thread(name=t.name, target=t._Thread__target, args = t.args)
                new_t = OwnTimer(0, name=t.name, function=t.function, args = t.args)
                new_t.start()
                threadliste.remove(t)
                threadliste.append(new_t)
    time.sleep(20)