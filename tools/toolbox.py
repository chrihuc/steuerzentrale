#!/usr/bin/env python

import constants

import os
import threading
from socket import gethostbyname
import re, sys
import time
from time import localtime,strftime
from datetime import date
import inspect
import uuid
import copy
#pycurl
#import urllib3
#from urllib.request import urlopen

from threading import Thread, Event
#
class OwnTimer(Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, name, failed=False, restartCounter=0, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.name = name
        self.failed = failed
        self.restartCounter = restartCounter
        self.heartbeat = 0
        self.args = args
        self.kwargs = kwargs
        self.starting = True
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()  


# TODO: unittest

logfolder = constants.installation_folder + "/log/"
homefolder = constants.installation_folder
selfsupervision = True


def main():
    print(check_ext_ip())
    print (ping("127.0.0.1"))

def ping(IP, number = 1):
    pinged = False
    if IP == None:
        return False
    else:
        lifeline = re.compile(r"(\d) received")
        for i in range(0,number):
            pingaling = os.popen("ping -q -c 2 "+IP,"r")
            sys.stdout.flush()
            while 1==1:
               line = pingaling.readline()
               if not line: break
               igot = re.findall(lifeline,line)
               if igot:
                if int(igot[0])==2:
                    pinged = True
                else:
                    pass
        return pinged

def log(*args, **kwargs):     
    if 'level' not in kwargs:
        level=9
    else:
        level=kwargs['level']
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)     
    if constants.debug_text != '':
        if not constants.debug_text in calframe[1][1] and not constants.debug_text in calframe[1][3]:
            return    
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    data = {"Description":args, "ts":uhr}
    data['Func1'] = calframe[1][1]
    data['Func2'] = calframe[1][3] 
#    mqtt_pub("log/Prio" + str(level), data)       
    if level > constants.debug_level:
        return
    if constants.debug:
        print('%s [%s, %s] %s %s' % (uhr, calframe[1][1], calframe[1][3], level, args))
#def restart_services():
  #lgd = logdebug(True, True)
  #lgd.debug("Heartbeat supervision")
  #if selfsupervision:
    #exectext = "sudo " + homefolder + "restart_services.sh"
    #lgd.log("Restart services")
    #os.system(exectext)

#def restart_wecker():
  #lgd = logdebug(True, True)
  #lgd.debug("Wecker neustart")
  #if selfsupervision:
    #exectext = "sudo " + homefolder + "restart_wecker.sh"
    #lgd.log("Restart Wecker")
    #os.system(exectext)

#def sendmail(betreff, text):
    #msg = MIMEText(text)
    #msg["From"] = "chrihuc@gmail.com"
    #msg["To"] = "chrihuc@gmail.com"
    #msg["Subject"] = betreff
    #p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    #p.communicate(msg.as_string())

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

def kw_unpack(kwargs, searched_key):
    if searched_key in kwargs:
        return kwargs[searched_key]
    return False

def sleep(interval):
    counter = 0
    try:
        while constants.run and counter < interval:
            time.sleep(1)
            counter += 1
    except KeyboardInterrupt:
        constants.run = False

def restart():
    constants.run = False
    exectext = "sudo svc -du /etc/service/steuerzentrale"
    os.system(exectext)    
    exectext = "sudo killall python3"
    os.system(exectext)
    sys.exit()    

class communication(object):

    queue = []
    callbacks = {}

    @classmethod
    def register_callback(cls, func):
        hash_id = str(uuid.uuid4())
        cls.callbacks[hash_id] = {'func':func,'active':True}
        return hash_id
    
    @classmethod
    def unregister_callback(cls, hash_id):
        cls.callbacks[hash_id]['active']=False
        return True

    @classmethod
    def send_message(cls, payload, *args, **kwargs):
        log(payload, args, kwargs, level=9)
        for hash_id, callbackdict in cls.callbacks.items():
            if args:
                args_to_send =[payload].append(args)
            else:
                args_to_send =[payload]
            if callbackdict['active']:
                t = threading.Thread(target=callbackdict['func'], args=args_to_send, kwargs=kwargs)
                t.start()
#            callback(payload, *args, **kwargs)

class meas_value:
    def __init__(self):
        self.data = []
        self.count = 0
        self.avg = 0
        self.min = 10000
        self.max = -10000
        self.last = 0
        self.act = 0
        self.alarm = 0

    def new_value(self,new):
        self.last = self.act
        self.count = self.count + 1
        self.avg = (self.avg*(self.count-1) + new)/self.count
        if new < self.min: self.min = new
        if new > self.max: self.max = new
        self.act = new

    def reset(self):
        self.count = 0
        self.avg = 0
        self.min = 10000
        self.max = -10000

class logdebug:
    def __init__(self, logging, debugging):
        self.logging = logging
        self.debugging = debugging


    def debug(self, text):
        if self.debugging:
            zeit =  time.time()
            datum = date.today()
            datei = logfolder + 'controller' + str(datum) + '.log'
            f = open(datei, 'a')
            f.write('\n' + str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))+ str(text))
            f.closed

    def log(self, text):
        if self.logging:
            zeit =  time.time()
            datum = date.today()
            datei = logfolder + 'controller' + str(datum) + '.log'
            f = open(datei, 'a')
            f.write('\n' + str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))+ str(text))
            f.closed


if __name__ == '__main__':
    main()

