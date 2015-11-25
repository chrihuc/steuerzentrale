#!/usr/bin/env python

import constants

import httplib,xml,urllib2,subprocess,os
from socket import gethostbyname
import json
import re, os, sys
import time
from time import localtime,strftime
from datetime import date
#pycurl


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
        report = ("No response","Partial Response","Alive")         
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

class myezcontrol:
    def __init__(self,ip,user,passwd):
        self.data = []
        self.ip_add = str(ip)
        self.usern=user
        self.password = passwd
        
    def SetSwitch(self,Switch,Wert):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&value=""" + str(Wert)
        f = urllib2.urlopen(body)

    def SetSwitchFunction(self,Switch,Function):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&Function=""" + str(Function)
        f = urllib2.urlopen(body)        
        
    def GetSwitch(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_actuator&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        return Wert
        f.close()    
        
    def GetBattery(self,name):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(name)
        f = urllib2.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        decoded = json.loads(html)
        battery = decoded['sensor']['state']
        status = battery[0]
        dict = {'battery':battery}
        return status        
        
    def GetSensor(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        return Wert
        f.close()       

    def GetSensor_neu(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"state":')
        Wert = html [position1+9:position2-4]
        return Wert
        f.close()         
        
    def GetTimer(self,name):
        body = """http://""" + self.ip_add + """/control?user=""" + self.usern + """&pwd=""" + self.password + """&cmd=get_config_timer&name=""" +name + """&callback=cname"""
        f = urllib2.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        decoded = json.loads(html)
        enabled = decoded['timer']['type']
        number = decoded['timer']['number']
        weekdays = decoded['timer']['weekdays']
        time = decoded['timer']['time']
        random = decoded['timer']['random']
        offset = decoded['timer']['offset']
        earliest = decoded['timer']['earliest']
        latest = decoded['timer']['latest']
        actuator = decoded['timer']['actuator']
        dict = {'enabled':enabled,'number':number,'weekdays':weekdays,'time':time,'random':random,'offset':offset,'earliest':earliest,'latest':latest,'actuator':actuator}
        return dict
        #print dict.get('enabled')
        #weekdays = dict.get('weekdays')
        #for n in weekdays:
        #    print n
        
        
    def SetTimer(self,enable,number,name,weekdays,hour,minute,sec,offset,random,earliest,latest,actname,function):
        #enable = disabled,time
        body1 = """http://""" + self.ip_add + """/control?user=""" + self.usern + """&pwd=""" + self.password 
        body2 = """&v=16&cmd=SET_CONFIG_TIMER&number=""" + number + """&type="""+ enable +"""&name="""+ name
        body3 = """&weekdays=""" + weekdays + """&hour=""" + hour + """&min=""" + minute + """&sec=""" + sec
        body4 = """&offset=""" + offset + """&random=""" + random + """&earliest=""" + earliest + """&latest=""" + latest
        body5 = """&actuator.name=""" + actname + """&actuator.function=""" + function + """&callback=JSON133"""
        body = body1 + body2 + body3 + body4 + body5
        f = urllib2.urlopen(body)
        #html = f.read()
        #print html

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
		
