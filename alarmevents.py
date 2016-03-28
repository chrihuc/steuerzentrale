#!/usr/bin/env python

import constants

import MySQLdb as mdb
from mysql_con import setting_r
from messaging import messaging
from threading import Timer
import threading
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import time

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




def main():
    aes = alarm_event()
    
    aes.new_event(description="anderer Alarm", prio=0)
    
    #acknowledge_alarm(alarm_id=1)
    
    #acknowledge_all()
    
    #alarms = aes.alarm_events_read(unacknowledged=True, prio=1)
    #for alarm in alarms:
    #    print alarm.get("description")
    
    #print alarm_events_read()
    
    aes.check_liste()

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns

table    = sql_object("HIS_alarmevents", "Historic", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"), ("Description","TEXT"),("Prio","DECIMAL(2,0)"),("Date","DATETIME"),("Acknowledged","DATETIME")))

class alarm_event:
    def __init__(self):
        self.__init_table__()
        self.mes = messaging()
        #self.mySocket = socket( AF_INET, SOCK_DGRAM )
        #self.OUTPUTS_IP   = '192.168.192.10'
        #self.OUTPUTS_PORT = 5000
        #self.szs = set_szene()

    def __init_table__(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+table.name+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+table.name +"("
                for num, col in enumerate(table.columns):
                    if num == len(table.columns)-1:
                        for co in col:
                            command += co + " "
                        command +=  ");"
                    else:
                        for co in col:
                            command += co + " "                    
                        command +=  ", "
                cur.execute(command)
                results = cur.fetchall()      
        con.close() 

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
            XS1DB = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
            with XS1DB:
                cur = XS1DB.cursor()
                if prio < 1:
                    insertstatement = 'INSERT INTO '+table.name+'(description, prio, acknowledged, Date) VALUES("' + str(description) + '", "' + str(prio) + '", CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)'
                else:
                    insertstatement = 'INSERT INTO '+table.name+'(description, prio, Date) VALUES("' + str(description) + '", "' + str(prio) + '", CURRENT_TIMESTAMP)'
                cur.execute(insertstatement)
            if str(setting_r("Status")) == "Wach":
                anwesend = True
            else:
                anwesend = False
            if prio == 0:
                pass
            elif prio == 1:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)
            elif prio == 2:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)                
            elif prio > 2 and prio < 3:
                self.mes.send_zuhause(to=self.mes.alle, titel="Hinweis", text=description)              
            elif prio == 3:
                self.mes.send_wach(to=self.mes.alle, titel="Achtung", text=description)
            elif prio > 3 and prio < 4:
                self.mes.send_wach(to=self.mes.alle, titel="Achtung", text=description)                  
            elif prio >= 4 and prio < 5:
                self.mes.send_direkt(to=self.mes.alle, titel="Alarm", text=description)
                msg = MIMEText(description)
                msg["From"] = constants.mail_.receiver
                msg["To"] = constants.mail_.receiver
                msg["Subject"] = "Alarm"
                p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
                p.communicate(msg.as_string())                 
            elif prio >= 5 and prio < 6:
                self.mes.send_direkt(to=self.mes.chris, titel="Alarm", text=description)                    
                
    def alarm_resolved(self, description, resolv_desc):
        alarme = self.alarm_events_read(unacknowledged=True,prio=1, time=24)
        for alarm in alarme:
            if description == alarm.get("description"):
                alarm_id = alarm.get("id")
                self.acknowledge_alarm(alarm_id)
                self.new_event(resolv_desc, prio=0)      
            
    def acknowledge_alarm(self, alarm_id):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE '+table.name+' SET acknowledged = CURRENT_TIMESTAMP WHERE id = '+ str(alarm_id) 
            cur.execute(sql)
        con.close() 

    def acknowledge_alarm_name(self, alarm_name):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE '+table.name+' SET acknowledged = CURRENT_TIMESTAMP WHERE description = '+ str(alarm_name) 
            cur.execute(sql)
        con.close()         
        
    def acknowledge_all(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE '+table.name+' SET acknowledged = CURRENT_TIMESTAMP WHERE acknowledged is NULL'
            cur.execute(sql)        
        con.close()
        #self.mySocket.sendto('az_Hinweis_gesehen',(self.OUTPUTS_IP,self.OUTPUTS_PORT))

    def alarm_events_read(self, unacknowledged=False, prio=0, time=24*60):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        liste = []
        with con:
            cur = con.cursor()
            if unacknowledged:
                sql = 'SELECT * FROM '+table.name+' WHERE acknowledged is NULL AND prio >= ' + str(prio) +' AND date > DATE_ADD(NOW(), INTERVAL -' + str(time) + ' MINUTE) ORDER BY ID DESC'
            else:
                sql = 'SELECT * FROM '+table.name+' WHERE prio >= ' + str(prio) +' AND date > DATE_ADD(NOW(), INTERVAL -' + str(time) + ' MINUTE) ORDER BY ID DESC'
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
