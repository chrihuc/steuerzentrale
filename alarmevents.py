#!/usr/bin/env python

import constants

#import MySQLdb as mdb
#from mysql_con import mdb_sonos_r, mdb_sonos_s, mdb_szene_r, mdb_hue_r, setting_s, setting_r, mdb_marantz_r, mdb_hue_s, mdb_fern_schluessel_r
#from messaging import messaging
#from socket import socket, AF_INET, SOCK_DGRAM
#from threading import Timer
#import threading
#from phue import Bridge
#import subprocess
#from email.mime.text import MIMEText
#from subprocess import Popen, PIPE
#import time
#from szenen import set_szene

# 4 prios at the moment
# 0 no action
# 0.1 with red light notification
# 0.2 with blue light notification
# 0.3 with green light notification

# 1 send notification to at home and once in 24h

# 2

# 3 send notification only when awake


# 4 send notification all times

# * todo:
# * 4.0 no light
# * 4.1 lights red 30 secs
# * 4.2 lights red in anticipation (Schlafzimmer only when not awake)
# * 4.3 lights blinking red in higher alarm, same as above
hue_devices =['Stehlampe','Stablampe 1', 'Stablampe 2', 'LightStrips 2']
hbridge = Bridge('192.168.192.190')

def hue_set_szene(device, szene):
    if szene == 'Save': 
        hue = hbridge.get_light(device, 'hue')
        bri = hbridge.get_light(device, 'bri')
        sat = hbridge.get_light(device, 'sat')
        an = hbridge.get_light(device, 'on') 
        #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
        setting = {'hue': hue, 'bri': bri, 'sat': sat, 'an': an}
        mdb_hue_s(device, setting)
        return
    keys = ['bri', 'hue', 'sat', 'transitiontime']
    szene = mdb_hue_r(szene)
    if str(szene.get('an')) == "1" or str(szene.get('an')) == "True":
        hbridge.set_light(device, {'on':True}) 
    command = {}
    for key in keys:
        if ((szene.get(key) <> "") and (str(szene.get(key)) <> "None")):
            command[key] = szene.get(key)
    if command <> {}:
        hbridge.set_light(device, command)
    if str(szene.get('an')) == "0" or str(szene.get('an')) == "False":
        hbridge.set_light(device, {'on':False}) 

def main():
    aes = alarm_event()
    
    aes.new_event(description="anderer Alarm", prio=1.3)
    
    #acknowledge_alarm(alarm_id=1)
    
    #acknowledge_all()
    
    #alarms = aes.alarm_events_read(unacknowledged=True, prio=1)
    #for alarm in alarms:
    #    print alarm.get("description")
    
    #print alarm_events_read()
    
    aes.check_liste()

class alarm_event:
    def __init__(self):
        self.mes = messaging()
        self.mySocket = socket( AF_INET, SOCK_DGRAM )
        self.OUTPUTS_IP   = '192.168.192.10'
        self.OUTPUTS_PORT = 5000
        #self.szs = set_szene()

    def new_event(self, description, prio=0, durchsage="", karenz=-1):
        t = threading.Thread(target=self.new_event_t, args=[description, prio, durchsage, karenz])
        t.start() 
    
    def new_event_t(self, description, prio=0, durchsage="", karenz=-1):
        if prio < 0: return
        if karenz == -1:
            if prio == 1:
                alarme = self.alarm_events_read(unacknowledged=True,prio=1, time=24*60)
            else:
                alarme = self.alarm_events_read(unacknowledged=True,prio=1, time=60)
        else:
            alarme = self.alarm_events_read(prio=int(prio), time=karenz)
        neuer = True
        for alarm in alarme:
            if description == alarm.get("description"):
                neuer = False
        if neuer:                
            dicti = {}
            XS1DB = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
            with XS1DB:
                cur = XS1DB.cursor()
                if prio < 1:
                    insertstatement = 'INSERT INTO alarm_events(description, prio, acknowledged) VALUES("' + str(description) + '", "' + str(prio) + '", CURRENT_TIMESTAMP)'
                else:
                    insertstatement = 'INSERT INTO alarm_events(description, prio) VALUES("' + str(description) + '", "' + str(prio) + '")'
                cur.execute(insertstatement)
            if str(setting_r("Status")) == "Wach":
                anwesend = True
            else:
                anwesend = False
            if prio == 0:
                pass
            elif prio > 1 and prio < 2:
                t =  Timer(0.1,self.hue_set, args=[prio *10 % 10])
                if anwesend and (str(setting_r("Notification_Visuell")) == "An"):
                    t.start() 
            elif prio == 1:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)
            elif prio == 2:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)                
            elif prio > 2 and prio < 3:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)
                t =  Timer(0.1,self.hue_blink_set, args=[prio *10 % 10, 2, 3])
                if anwesend and (str(setting_r("Notification_Visuell")) == "An"):
                    t.start()                   
            elif prio == 3:
                self.mes.send_wach(to=self.mes.alle, titel="Achtung", text=description)
            elif prio > 3 and prio < 4:
                self.mes.send_wach(to=self.mes.alle, titel="Achtung", text=description)
                t =  Timer(0.1,self.hue_blink_set, args=[prio *10 % 10, 3, 2])
                if anwesend and (str(setting_r("Notification_Visuell")) == "An"):
                    t.start()                    
            elif prio >= 3:
                self.mes.send_direkt(to=self.mes.alle, titel="Alarm", text=description)
                msg = MIMEText(description)
                msg["From"] = "chrihuc@gmail.com"
                msg["To"] = "chrihuc@gmail.com"
                msg["Subject"] = "Alarm"
                p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
                p.communicate(msg.as_string())                
            elif prio > 4:
                t =  Timer(0.1,self.hue_blink_set, args=[prio *10 % 10])
                if (str(setting_r("Notification_Visuell")) == "An"):
                    t.start() 
            if durchsage <> "":
                setting_s("Durchsage",durchsage)
                self.mySocket.sendto('az_Durchsage',(self.OUTPUTS_IP,self.OUTPUTS_PORT))

                
    def alarm_resolved(self, description, resolv_desc):
        alarme = self.alarm_events_read(unacknowledged=True,prio=1, time=24)
        for alarm in alarme:
            if description == alarm.get("description"):
                alarm_id = alarm.get("id")
                self.acknowledge_alarm(alarm_id)
                self.new_event(resolv_desc, prio=0)
                
    
    def hue_blink_set(self, farbe, Anzahl = 15, Pause = 1):
        i = 0
        for device in hue_devices:
            hue_set_szene(device, "Save")
        while i < Anzahl:
            for device in hue_devices:
                hue_set_szene(device, farbe)
            time.sleep(Pause)
            for device in hue_devices:
                hue_set_szene(device, "Aus")
            time.sleep(Pause)
            i = i + 1
        self.hue_reset()
    
    def hue_set(self, farbe):
        for device in hue_devices:
            hue_set_szene(device, "Save")
            hue_set_szene(device, farbe)
        t =  Timer(30,self.hue_reset)
        t.start()             
    
    def hue_reset(self):
        for device in hue_devices:
            hue_set_szene(device, device)        
            
    def acknowledge_alarm(self, alarm_id):
        con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
        with con:
            cur = con.cursor()
            sql = 'UPDATE alarm_events SET acknowledged = CURRENT_TIMESTAMP WHERE id = '+ str(alarm_id) 
            cur.execute(sql)
        con.close() 

    def acknowledge_alarm_name(self, alarm_name):
        con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
        with con:
            cur = con.cursor()
            sql = 'UPDATE alarm_events SET acknowledged = CURRENT_TIMESTAMP WHERE description = '+ str(alarm_name) 
            cur.execute(sql)
        con.close()         
        
    def acknowledge_all(self):
        con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
        with con:
            cur = con.cursor()
            sql = 'UPDATE alarm_events SET acknowledged = CURRENT_TIMESTAMP WHERE acknowledged is NULL'
            cur.execute(sql)        
        con.close()
        self.mySocket.sendto('az_Hinweis_gesehen',(self.OUTPUTS_IP,self.OUTPUTS_PORT))

    def alarm_events_read(self, unacknowledged=False, prio=0, time=24*60):
        con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
        dicti = {}
        liste = []
        with con:
            cur = con.cursor()
            if unacknowledged:
                sql = 'SELECT * FROM alarm_events WHERE acknowledged is NULL AND prio >= ' + str(prio) +' AND date > DATE_ADD(NOW(), INTERVAL -' + str(time) + ' MINUTE) ORDER BY ID DESC'
            else:
                sql = 'SELECT * FROM alarm_events WHERE prio >= ' + str(prio) +' AND date > DATE_ADD(NOW(), INTERVAL -' + str(time) + ' MINUTE) ORDER BY ID DESC'
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            j = 0
            for row in results:
                for i in range (0,len(row)):
                   #print row[i]
                   dicti[field_names[i]] = row[i]
                liste.append(dicti)
                dicti = {}
                j = j + 1
            return liste
        
    def check_liste(self):
        alarme = self.alarm_events_read(unacknowledged=True,prio=1)
        nachricht = " # "
        if len(alarme) > 0 :
            for alarm in alarme:
                nachricht =  nachricht + alarm.get("description") + " # "
            self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text="Es gibt " + str(len(alarme)) + " neue Alarme:" + nachricht)
        

if __name__ == '__main__':
    main()  
