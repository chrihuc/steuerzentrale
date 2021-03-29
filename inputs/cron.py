#!/usr/bin/env python

import constants


import time
from threading import Timer
import threading
from time import localtime,strftime
import datetime
from outputs import cron
#from outputs import szenen
from outputs import internal

from tools import toolbox
from outputs.mqtt_publish import mqtt_pub
#toolbox.log('debug on')

# TODO: unittest?

crn = cron.Cron()
#scenes = szenen.Szenen()

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
    toolbox.communication.send_message(payload, typ='InputValue')
    
def broadcast_exec_szn(szene):
    payload = {'Szene':szene}
#    on server:
    toolbox.communication.send_message(payload, typ='ExecSzene')    

def main():
    periodic_supervision()

def every_min(tag, zeit):
    toolbox.log(tag, zeit)
    liste = crn.get_now2(tag, zeit)
    for szene in liste:
        toolbox.log(szene)
        if str(szene.get('Szene')) != "None":
            lt = localtime()
            sekunde = int(strftime("%S", lt))
#            task = Timer(float(60-sekunde), scenes.execute, [str(szene.get('Szene'))])
            task = Timer(float(60-sekunde), broadcast_exec_szn, [str(szene.get('Szene'))])            
            task.start()
        if str(szene.get('Permanent')) == "False":
            crn.executed(szene.get('Id'))
    return True

def every_2_min():
    pass

def every_10_min():
    pass

def every_30_min():
    pass

def every_60_min():
    internal.check_ext_ip(False)
    pass

def every_24_hrs():
    crn.calculate()

def periodic_supervision():
    while constants.run:
        try:
        #executed every day
            lt = localtime()
            stunde = int(strftime("%H", lt))
            minute = int(strftime("%M", lt))
            sekunde = int(strftime("%S", lt))
            toolbox.sleep(60-sekunde)
            min2 = int((minute))
            min1 = 0
            l = 0
            if minute >= 30:
                min1 = 1
                min2 = (minute - 30)
            for k in range(stunde,24):
                lt = localtime()
                minute = int(strftime("%M", lt))
                min2 = int((minute))
                min1 = 0
                min10 = 0
                if minute >= 30:
                    min1 = 1
                    min2 = (minute - 30)
                for j in range(min1,2):
                    for i in range(min2,30):
                        #executed every min
                        zeit =  time.time()
                        uhr = str(strftime("%H:%M",localtime(zeit))) 
                        mqtt_pub("Time", {'Value':uhr})
                        jetzt = datetime.datetime.today()
                        jetzt = jetzt + datetime.timedelta(minutes=1)
                        tag = (jetzt.weekday() + 1) % 7
                        uhr = jetzt.strftime("%H:%M")                    
                        l += 1
                        if l == 2:
                            t = threading.Thread(target=every_2_min)
                            t.start()
                            l = 0
                        min10 += 1
                        if min10 == 10:
                            t = threading.Thread(target=every_10_min)
                            t.start()
                            min10 = 0
    #                    #check cron
    #                    tag = int(strftime("%w", lt))
    #                    #log(str(stunde_f_alarm))
    #                    if (j*30+i+1)>=60:
    #                        if k+1 >=24:
    #                            zeit = str(0) + ":" + str(0)
    #                            tag += 1
    #                        else:
    #                            zeit = str(k+1) + ":" + str(0)
    #                    else:
    #                        zeit = str(k) + ":" + str(j*30+i+1)
    #                    if tag == 7:
    #                        tag = 0
                        t = threading.Thread(target=every_min, args=[tag,uhr])
                        t.start()
                        lt = localtime()
                        sekunde = int(strftime("%S", lt))
                        toolbox.sleep(60-sekunde)
                    #executed every 30 min
                    t = threading.Thread(target=every_30_min)
                    t.start()
                    min2 = 0
                #executed every hour
                t = threading.Thread(target=every_60_min)
                t.start()
            min1 = 0
            #executed once 24 hrs
            t = threading.Thread(target=every_24_hrs)
            t.start()
        except Exception as e:
            print(e)            


if __name__ == '__main__':
    main()
