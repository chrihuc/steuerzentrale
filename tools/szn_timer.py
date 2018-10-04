# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 09:24:15 2016

@author: christoph
"""

# TODO: unpickle
import json
from threading import Timer
import datetime
import ast
#import pickle

from tools import toolbox

import datetime
import uuid


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

class Szenen_Timer:
        
    def __init__(self,callback=None):
        self.liste = []
        self._callback = callback
        self.load()
        #self.index_p = {}
        #self.index_c = {}
        #exact means parent needs to be the same
        #retrig means its possible to delay, or it is just a normal timer

    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self, callback):
        self._callback = callback

    def add_timer(self, parent, delay, child, exact, retrig, device, start=False):
        if delay == 0 and start:
            self.callback(child)
            return None
        ct = datetime.datetime.now()
        dicti = {}
        dicti["parent"] = parent
        dicti["device"] = device
        dicti["delay"] = delay
        dicti["child"] = child
        dicti["exact"] = exact
        dicti["retrig"] = retrig
        dicti['due'] = ct + datetime.timedelta(seconds=delay)
        hash_id = uuid.uuid4()
        dicti["hash_id"] = hash_id
        if delay < 0:
            self.cancel_timer(parent, child)
        else:
            t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child, device])
            dicti["timer"] = t
            if start: t.start()
            self.liste.append(dicti)
            self.store()
        return hash_id

    def start_timer(self, nr):
        item = self.liste[nr]
        item['due'] = datetime.datetime.now() + datetime.timedelta(0,self.liste[nr].get("delay"))
        self.store()
        self.liste[nr].get("timer").start()

    def add_timer_start(self, parent, delay, child, exact, retrig, device):
        return self.add_timer(parent, delay, child, exact, retrig, device, start=True)

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

    def retrigger(self, parent, delay, child, exact, retrig, device):
        found = False
        for item in self.liste:
            if item.get("parent") is None:
                if (item.get("device") == device or (not(item.get("exact")))) and item.get("child") == child:
                    if item.get("retrig"): item.get("timer").cancel()
                    hash_id = item.get("hash_id")
                    if delay > 0:
                        t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child, device])
                        item["timer"] = t
                        item['due'] = datetime.datetime.now() + datetime.timedelta(0,delay)
                        item.get("timer").start()
                        self.store()
                    else:
                        self.callback(child, device=device, wert='timed')
                        self.liste.remove(item)
                        self.store()
                    found = True                
            else:
                if (item.get("parent") == parent or (not(item.get("exact")))) and item.get("child") == child:
                    if item.get("retrig"): item.get("timer").cancel()
                    hash_id = item.get("hash_id")
                    if delay > 0:
                        t =  Timer(delay,self.entferne_eintrag, args=[hash_id, child, device])
                        item["timer"] = t
                        item['due'] = datetime.datetime.now() + datetime.timedelta(0,delay)
                        item.get("timer").start()
                        self.store()
                    else:
                        self.callback(child, device=device, wert='timed')
                        self.liste.remove(item)
                        self.store()
                    found = True
        return found

    def retrigger_add(self, parent, delay, child, exact=False, retrig=True, device=None):
        if not self.retrigger(parent, delay, child, exact, retrig, device):
            return self.add_timer_start(parent, delay, child, exact, retrig, device)

    def zeige(self):
        print(self.liste)

    def store(self):
        write_list = []
        for dicti in self.liste:
            new_dict = {}
            for key, value in dicti.items():
                if key not in ['timer', 'hash_id']:
                    new_dict[key] = value
            write_list.append(new_dict)
        with open('szn_timer.tmp', 'w') as f:
            f.write(str(self.liste))
        with open('szn_timer.jsn', 'w') as fout:
            json.dump(write_list, fout, default=json_serial)

    def load(self):
        try:
            with open('szn_timer.jsn') as f:
                full = f.read()            
            alte = json.loads(full)
            for eintrag in alte:
                due = datetime.datetime.strptime(eintrag['due'], '%Y-%m-%dT%H:%M:%S.%f')
                ct = datetime.datetime.now()
                if due > ct:
                    delay = (due - ct).seconds + 1
                    parent = eintrag['parent']
                    child = eintrag['child']
                    exact = eintrag['exact']
                    retrig = eintrag['retrig'] 
                    device = eintrag['device']
                    self.add_timer(parent, delay, child, exact, retrig, device, start=True)
        except:
            toolbox.log('Laden der Szenen fehlgeschlagen', level=1)

    def entferne_eintrag(self, hash_id, child, device):
        for item in self.liste:
            if item.get("hash_id") == hash_id:
                self.liste.remove(item)
        self.callback(child, device=device)
        self.store()

