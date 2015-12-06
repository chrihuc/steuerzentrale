#!/usr/bin/env python
 
from threading import Timer
import time

import datetime

liste = {}
global start_t

def print_it(it):
    print datetime.datetime.now() - start_t
    print it

def main():
    global start_t
    start_t = datetime.datetime.now()
    sz_t = szenen_timer(def_to_run = print_it)
    id_nr = sz_t.retrigger_add(parent = "Bad_ir",delay = 10, child = "Bad_aus")
    time.sleep(5)
    sz_t.retrigger_add(parent = "Bad_ir",delay = 15, child = "Bad_aus")
    
class szenen_timer:
    def __init__(self,def_to_run):
        self.liste = []
        self.def_to_run = def_to_run
        #self.index_p = {}
        #self.index_c = {}
        
    def add_timer(self, parent, delay, child):
        dicti = {}
        dicti["parent"] = parent
        dicti["delay"] = delay
        dicti["child"] = child
        t =  Timer(delay,self.def_to_run, args=[child])
        dicti["timer"] = t
        self.liste.append(dicti)
        return len(self.liste) - 1
        
    def start_timer(self, nr):
        self.liste[nr].get("timer").start()
        
    def add_timer_start(self, parent, delay, child):
        numm = self.add_timer(parent, delay, child)
        self.start_timer(numm)
        
    def stop_timer(self, nr):
        self.liste[nr].get("timer").cancel()        
        
    def retrigger(self, parent, delay, child):
        found = False
        for item in self.liste:
            if item.get("parent") == parent and item.get("child") == child:
                item.get("timer").cancel()
                t =  Timer(delay,self.def_to_run, args=[child])
                item["timer"] = t
                item.get("timer").start()
                found = True
        return found   
    
    def retrigger_add(self, parent, delay, child):
        if not self.retrigger(parent, delay, child):
            self.add_timer_start(parent, delay, child)
        
if __name__ == '__main__':
    main()  