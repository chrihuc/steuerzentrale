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
#pycurl
import urllib2

def check_ext_ip():
    ext_ip = urllib2.urlopen('http://whatismyip.org').read()
    match = '(([0-9]{1,3}\.){3}[0-9]{1,3})'
    m = re.search(match, ext_ip)
    if m:
        found = m.group(1)
        return found
    return '0.0.0.0'

# TODO: unittest

logfolder = constants.installation_folder + "/log/"
homefolder = constants.installation_folder
selfsupervision = True


def main():
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
    if level > constants.debug_level:
        return
    if constants.debug:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if constants.debug_text <> '':
            if not constants.debug_text in calframe[1][1] and not constants.debug_text in calframe[1][3]:
                return
        zeit =  time.time()
        uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
        print '%s [%s, %s] %s' % (uhr, calframe[1][1], calframe[1][3], args)
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

class communication(object):

    queue = []
    callbacks = []

    @classmethod
    def register_callback(cls, func):
        cls.callbacks.append(func)

    @classmethod
    def send_message(cls, payload, *args, **kwargs):
        log(payload, args, kwargs, level=3)
        for callback in cls.callbacks:
            if args:
                args_to_send =[payload].append(args)
            else:
                args_to_send =[payload]
            t = threading.Thread(target=callback, args=args_to_send, kwargs=kwargs)
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

