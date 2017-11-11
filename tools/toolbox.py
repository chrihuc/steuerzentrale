#!/usr/bin/env python

import constants

import os
from socket import gethostbyname
import re, sys
import time
from time import localtime,strftime
from datetime import date
import inspect
#pycurl

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

def log(text='', level=0):
    if constants.debug:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print '[%s, %s] %s' % (calframe[1][1], calframe[1][3], text) 
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

