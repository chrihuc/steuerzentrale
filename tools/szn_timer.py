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

# TODO: pickle, unittest

from threading import Timer
import time
import pickle

import datetime
import uuid

liste = {}
global start_t

def print_it(it):
    print datetime.datetime.now() - start_t, it

def main():
    global start_t
    start_t = datetime.datetime.now()
    sz_t = Szenen_Timer(def_to_run = print_it)
    print sz_t.retrigger_add(parent = "Bad_ir",delay = 10, child = "Bad_aus", exact = False, retrig = True)
    time.sleep(5)
#    sz_t.cancel_timer(parent = "Bad_i", child = "Bad_aus")
    sz_t.zeige()

class Szenen_Timer:
    def __init__(self,def_to_run):
        self.liste = []
        self.def_to_run = def_to_run
        #self.index_p = {}
        #self.index_c = {}
        #exact means parent needs to be the same
        #retrig means its possible to delay, or it is just a normal timer

    def add_timer(self, parent, delay, child, exact, retrig,  start=False):
        if delay == 0 and start:
            self.def_to_run(child)
            return None
        dicti = {}
        dicti["parent"] = parent
        dicti["delay"] = delay
        dicti["child"] = child
        dicti["exact"] = exact
        dicti["retrig"] = retrig
        hash_id = uuid.uuid4()
        dicti["hash_id"] = hash_id
        if delay < 0:
            self.cancel_timer(parent, child)
        else:
            t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child])
            dicti["timer"] = t
            if start: t.start()
            self.liste.append(dicti)
        return hash_id

    def start_timer(self, nr):
        #print self.liste, nr
        item = self.liste[nr]
        item['due'] = datetime.datetime.now() + datetime.timedelta(0,self.liste[nr].get("delay"))
        self.store()
        self.liste[nr].get("timer").start()

    def add_timer_start(self, parent, delay, child, exact, retrig):
        return self.add_timer(parent, delay, child, exact, retrig, start=True)

    def stop_timer(self, nr):
        self.liste[nr].get("timer").cancel()

    def cancel_timer(self,parent,child):
        found = False
        for item in self.liste:
            if (item.get("parent") == parent or (not(item.get("exact")))) and item.get("child") == child:
                item.get("timer").cancel()
                self.liste.remove(item)
                self.store()
                found = True
        return found

    def retrigger(self, parent, delay, child, exact, retrig):
        found = False
        for item in self.liste:
            if (item.get("parent") == parent or (not(item.get("exact")))) and item.get("child") == child:
                if item.get("retrig"): item.get("timer").cancel()
                hash_id = item.get("hash_id")
                if delay > 0:
                    t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child])
                    item["timer"] = t
                    item['due'] = datetime.datetime.now() + datetime.timedelta(0,delay)
                    item.get("timer").start()
                    self.store()
                else:
                    self.def_to_run(child)
                    self.liste.remove(item)
                    self.store()
                found = True
        return found

    def retrigger_add(self, parent, delay, child, exact = False, retrig = True):
        if not self.retrigger(parent, delay, child, exact, retrig):
            return self.add_timer_start(parent, delay, child, exact, retrig)

    def zeige(self):
        print self.liste

    def store(self):
        file_ = open('szn_timer.tmp', 'w')
        file_.write(str(self.liste))
        file_.close()

    def entferne_eintrag(self, hash_id, child):
        for item in self.liste:
            if item.get("hash_id") == hash_id:
                self.liste.remove(item)
        self.def_to_run(child)
        self.store()

if __name__ == '__main__':
    main()