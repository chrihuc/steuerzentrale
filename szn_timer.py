# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 09:24:15 2016

@author: christoph
"""

#neue idee kann aber dann nicht szene als task to run setzen
#((szene,zeit,retrigger))
#retrigger 0,1,2
#retrigger erhoeht um 1
#liste mit origin, destination, trg_count

#alte idee:

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
    sz_t.retrigger_add(parent = "Bad_ir",delay = 10, child = "Bad_aus", exact = False, retrig = True)
    time.sleep(5)
    sz_t.retrigger_add(parent = "Bad_i",delay = 10, child = "Bad_aus")
    sz_t.zeige()
    
class szenen_timer:
    def __init__(self,def_to_run):
        self.liste = []
        self.def_to_run = def_to_run
        #self.index_p = {}
        #self.index_c = {}
        #exact means parent needs to be the same
        #retrig means its possible to delay, or it is just a normal timer
        
    def add_timer(self, parent, delay, child, exact, retrig):
        dicti = {}
        dicti["parent"] = parent
        dicti["delay"] = delay
        dicti["child"] = child
        dicti["exact"] = exact
        dicti["retrig"] = retrig
        hash_id = "asbfaer"
        dicti["hash_id"] = hash_id     
        t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child])
        dicti["timer"] = t
        self.liste.append(dicti)
        return len(self.liste) - 1
        
    def start_timer(self, nr):
        self.liste[nr].get("timer").start()
        
    def add_timer_start(self, parent, delay, child, exact, retrig):
        numm = self.add_timer(parent, delay, child, exact, retrig)
        self.start_timer(numm)
        
    def stop_timer(self, nr):
        self.liste[nr].get("timer").cancel()        
        
    def retrigger(self, parent, delay, child, exact, retrig):
        found = False
        for item in self.liste:
            if (item.get("parent") == parent or (not(item.get("exact")))) and item.get("child") == child:
                if item.get("retrig"): item.get("timer").cancel()
                hash_id = item.get("hash_id")
                if delay > 0:
                    t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child])
                    item["timer"] = t
                    item.get("timer").start()
                else:
                    pass
                    #loesche ientrag
                found = True
        return found   
    
    def retrigger_add(self, parent, delay, child, exact = False, retrig = True):
        if not self.retrigger(parent, delay, child, exact, retrig):
            self.add_timer_start(parent, delay, child, exact, retrig)

    def zeige(self):
        for item in self.liste:  
            print item
        
    def entferne_eintrag(self, hash_id, child):
        #entferten eintra
        self.def_to_run(child)
      
if __name__ == '__main__':
    main()  