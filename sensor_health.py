#!/usr/bin/env python

import constants

from classes import myezcontrol
import MySQLdb as mdb
from alarmevents import alarm_event


ezcontrol = myezcontrol(constants.xs1_.IP,constants.xs1_.USER,constants.xs1_.PASS)
threshold = 250
threshold_balk = 100
threshold_TVcont = 50
aes = alarm_event()
#add evalatuion when the last start was.

def main():
    print check_TuerSpy_health(30)

def check_sensor_health():
    #if (ezcontrol.GetBattery("Haustuer") <> "ok"):
    #    aes.new_event(description="Leere Battery in Haustuer", prio=1.3, karenz=24*60)
    #if (ezcontrol.GetBattery("Balkontuer") <> "ok"):
    #    aes.new_event(description="Leere Battery in Balkontuer", prio=1.3, karenz=24*60)        
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM `XS1DB`.`Wohnzimmer_T` WHERE Date > DATE_ADD(NOW(), INTERVAL -4 HOUR)'
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) < threshold:
            aes.new_event(description="Problem mit Temperatur Wohnzimmer", prio=1.3, karenz=24*60)
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM `XS1DB`.`Schlafzimmer_T` WHERE Date > DATE_ADD(NOW(), INTERVAL -4 HOUR)'
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) < threshold:
            aes.new_event(description="Problem mit Temperatur Schlafzimmer", prio=1.3, karenz=24*60)         
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM `XS1DB`.`Balkon_T` WHERE Date > DATE_ADD(NOW(), INTERVAL -4 HOUR)'
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) < threshold_balk:
            aes.new_event(description="Problem mit Temperatur Balkon", prio=1.3, karenz=24*60)        
    con.close     

def check_TVControl_health(time):        
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    ergebnis = 0
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM XS1DB.Actuators where Name like "Hellig%" and Date > DATE_ADD(NOW(), INTERVAL -'+ str(time) +' MINUTE)'
        cur.execute(sql)
        results = cur.fetchall()
        ergebnis = len(results)
    con.close
    return ergebnis

def check_TuerSpy_health(time):        
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    ergebnis = 0
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM XS1DB.Actuators where Name like "Haustuer_static" and Date > DATE_ADD(NOW(), INTERVAL -'+ str(time) +' MINUTE)'
        cur.execute(sql)
        results = cur.fetchall()
        ergebnis = len(results)
    con.close
    return ergebnis
    
if __name__ == '__main__':
    main()
