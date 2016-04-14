#!/usr/bin/env python

import constants

#import sensor_health
#from alarmevents import alarm_event
import time
from threading import Timer
import threading
#from checkraid import checkraid
from time import localtime,strftime
#from mysql_con import  setting_r
from cron import cron
#from datetime import date
#import os
#from dateutil.relativedelta import relativedelta
#import shutil, glob
#from messaging import messaging
#from webcammov import mail_webc_pics
#from anwesenheit import anwesenheit
#from plexapi.server import PlexServer
from cmd_szenen import szenen
#import satellites


#aes = alarm_event()
crn = cron()
scenes = szenen()
#mes = messaging()
#status = anwesenheit()
#plex = PlexServer()
tv_con_check_old = 0
#sats = satellites.get_satellites()

def main():
    periodic_supervision()
    #print crn.get_now(4, "18:22", "cron")
    #every_min(4, "18:22", "cron")
    #every_30_min()
    #crn.calculate()
    #every_10_min()
                
    
def every_min(tag, zeit):
    liste = crn.get_now2(tag, zeit)
    for szene in liste:
        if str(szene.get('Szene')) <> "None":
            lt = localtime()
            sekunde = int(strftime("%S", lt))                     
            task = Timer(float(60-sekunde), scenes.execute, [str(szene.get('Szene'))])              
            task.start()
        if str(szene.get('Permanent')) == "False":
            crn.delete(szene.get('Id'))  
    #if str(setting_r("Kino_Beleuchtung_Auto")) == "Ein":
        #if plex.sessions() == []:
                #if str(setting_r("Kino_Beleuchtung")) == "Ein":
                    #set_szene("AutoBelEin")
        #else:
            #if str(setting_r("Kino_Beleuchtung")) == "Aus":
                #set_szene("Kino_BeleuchtungSet")

def every_2_min():
    pass
#    akt_status = status.check_all()
#    if (akt_status.get("Anwesenheit") == 0) and  not (str(setting_r("Status")) in ["Besuch", "Abwesend", "Gegangen"]):
#        aes.new_event(description="Neue Anwesenheit regel: Abwesend", prio=0)
#        set_szene("Alles_aus_4")
#    if (akt_status.get("Anwesenheit") < 0) and  not (str(setting_r("Status")) in ["Besuch", "Urlaub"]):
#        aes.new_event(description="Neue Anwesenheit regel: Urlaub", prio=0)

def every_10_min():
    pass
#    for sat in sats:
#        if sat.Type == "sat":
#            no_hbts = sensor_health.check_sat_health(sat.name,30)
#            if no_hbts <= sat.no_of_lb and no_hbts < 4:
#                sat.reboot()             
#            elif no_hbts <= sat.no_of_lb and no_hbts < 25:
#                sat.kill_python()
#            sat.no_of_lb = no_hbts
        
        
def every_30_min():
    pass
#    if (str(setting_r("Status")) in ["Schlafen", "Abwesend", "Urlaub"]): mail_webc_pics()
#    sensor_health.check_sensor_health() 

def every_60_min():
    pass
    
def every_24_hrs():
        crn.calculate()
#        if constants.automatic_backup:
#            source = '/home/chris/homecontrol'
#            datum = date.today()
#            delete = date.today() - relativedelta(days=7)
#            destin = '/mnt/array1/MIsc/MySQL/'
#            fname = destin + str(datum)
#            if not os.path.exists(fname):
#                    os.makedirs(fname)    
#            datei = fname  + '/xs1db.sql'
#            #cmd = '/usr/bin/mysqldump -u root -p XS1DB > ' + datei
#            #os.system(cmd)
#            #datei = fname  + '/Gesundheit.sql'
#            #cmd = '/usr/bin/mysqldump -u root -p Gesundheit > ' + datei
#            #os.system(cmd)    
#            for filename in glob.glob(os.path.join(source, '*.py')):
#                    shutil.copy(filename, fname)
#            shutil.rmtree(destin + str(delete))
#            aes.new_event("Raidcheck: " + checkraid(), prio=0) 
#
#            source = '/mnt/array1/photos/SP3_pictures/'
#            destin = '/mnt/array1/photos/Database/'
#            datum = date.today()
#            delete = date.today() - relativedelta(days=31)  
#            photo_db = source + 'digikam4.db'
#            photo_db_newname = destin + 'digikam4_' + str(datum) + '.db'
#            shutil.copy(photo_db, photo_db_newname) 
#            photo_db_delete = destin + 'digikam4_' + str(delete) + '.db'
#            try:
#                    os.remove(photo_db_delete)
#            except:
#                    pass
    
def periodic_supervision():
    while constants.run:
        #executed every day
        lt = localtime()
        stunde = int(strftime("%H", lt))
        minute = int(strftime("%M", lt))
        sekunde = int(strftime("%S", lt))
        time.sleep(60-sekunde)
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
                    #check cron
                    tag = int(strftime("%w", lt))
                    #log(str(stunde_f_alarm))  
                    if (j*30+i+1)>=60:
                        if k+1 >=24:
                            zeit = str(0) + ":" + str(0)
                            tag += 1
                        else:
                            zeit = str(k+1) + ":" + str(0)
                    else:       
                        zeit = str(k) + ":" + str(j*30+i+1)
                    if tag == 7:
                        tag = 0 
                    t = threading.Thread(target=every_min, args=[tag,zeit])
                    t.start() 
#                    t = threading.Thread(target=every_min, args=[tag,zeit,"Wecker"])
#                    t.start()                    
                    lt = localtime()
                    sekunde = int(strftime("%S", lt))                    
                    time.sleep(60-sekunde)
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
        

if __name__ == '__main__':
    main() 
