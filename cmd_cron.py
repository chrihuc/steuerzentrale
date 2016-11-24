#!/usr/bin/env python

import constants

import MySQLdb as mdb
import ephem
from time import localtime,strftime,strptime
import datetime
import random


def main():
    crn = cron()
    #crn.new_event('Test','20:15')
    #print crn.get_now(2, '5:40' ,'Wecker')
    crn.calculate()
    print crn.get_all()
#    next_i = crn.get_next(2, '23:21')
#    if next_i: print next_i[0].get("delta")
#    print next_i

neuenh = ephem.Observer()
neuenh.lon  = str(9.036199)
neuenh.lat  = str(46.361999)  
neuenh.elev = 400

class cron:
    def __init__(self):
        pass
        
    def get_now(self, tag, Zeit, db=constants.sql_tables.cron.name):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        tage = {1:"Mo",2:"Di",3:"Mi",4:"Do",5:"Fr",6:"Sa",0:"So"}
        liste = []    
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM '+db+' WHERE ' + tage.get(tag) + '=True AND Time = "' + str(Zeit) + '" AND Eingeschaltet =True'
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
        con.close
        return liste 
    
    def get_all(self, db=constants.sql_tables.cron.name, wecker=False):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        liste = []    
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM '+constants.sql_tables.cron.name
            if wecker:
                sql = 'SELECT * FROM '+constants.sql_tables.cron.name+ ' WHERE Wecker ="True"'
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
        con.close
        return liste    

    def get_next(self, tag, Zeit, db=constants.sql_tables.cron.name, wecker = False):
        liste = self.get_all(wecker=wecker)
        ret_item = {}
        ret_liste = []
        tage = {1:"Mo",2:"Di",3:"Mi",4:"Do",5:"Fr",6:"Sa",0:"So"}
        Zeit = datetime.timedelta(hours=int(Zeit[:Zeit.find(":")]), minutes=int(Zeit[Zeit.find(":")+1:]), seconds=0)
        next_one = datetime.timedelta(hours=12, minutes=0, seconds=0)
        nulltime = datetime.timedelta(hours=0, minutes=0, seconds=0)
        morgen = tag + 1
        if morgen == 7: morgen = 0
        for eintrag in liste:
            if str(eintrag.get("Eingeschaltet")) <> "True" : continue
            if db == "Wecker":
                time = eintrag.get("Time") - eintrag.get("Offset")
            else:
                time = eintrag.get("Time")                        
            if (str(eintrag.get(tage.get(tag))) == "True"):
                if ((time - Zeit) ==  next_one) and (time - Zeit) >= nulltime : 
                    ret_item = eintrag
                    next_one = (time - Zeit)
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)
                elif ((time - Zeit) <  next_one) and (time - Zeit) >= nulltime : 
                    ret_liste = []
                    ret_item = eintrag
                    next_one = (time - Zeit)
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)                    
            if (str(eintrag.get(tage.get(morgen))) == "True"): 
                deltati = (time - Zeit) + datetime.timedelta(hours=24, minutes=0, seconds=0)
                if deltati == next_one: 
                    ret_item = eintrag
                    next_one = deltati
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)
                elif deltati < next_one: 
                    ret_liste = []
                    ret_item = eintrag
                    next_one = deltati
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)                    
        return ret_liste

    def get_now2(self, tag, Zeit, db=constants.sql_tables.cron.name):
        liste = self.get_next(tag, Zeit, db)
        if liste:
            if liste[0].get("delta") < datetime.timedelta(hours=0, minutes=1, seconds=0):
                return liste
        return []

    def delete(self, Id):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'DELETE FROM '+constants.sql_tables.cron.name+' WHERE id = '+ str(Id) 
            cur.execute(sql)
        con.close()

    def new_event(self, Szene, Time, Bedingung="", permanent=0):               
        dicti = {}
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            insertstatement = 'INSERT INTO '+constants.sql_tables.cron.name+'(Szene, Time, Bedingung, permanent) VALUES("' + str(Szene) + '", "' + str(Time) + '", "' + str(Bedingung) + '", "' + str(permanent) + '")'
            cur.execute(insertstatement)
        con.close
     
    def calculate(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        tage = {1:"Mo",2:"Di",3:"Mi",4:"Do",5:"Fr",6:"Sa",0:"So"}
        liste = []    
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM '+constants.sql_tables.cron.name
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
        con.close   
        lt = localtime()
        time = lt
        neuenh.date = strftime("%Y-%m-%d 00:00:00", lt)
        sunrise=(neuenh.next_rising(ephem.Sun())).datetime() + datetime.timedelta(hours=2, minutes=0, seconds=0)
        sunset =(neuenh.next_setting(ephem.Sun())).datetime() + datetime.timedelta(hours=2, minutes=0, seconds=0)
        for eintrag in liste:
            dynamic = False
            for setting in eintrag:
                if setting == "Sonne" and str(eintrag.get("Sonne")) <>  "None":
                    dynamic = True
                    if str(eintrag.get("Sonne")) == "rise":
                        time = sunrise.replace(second=0)
                    else:
                        time = sunset.replace(second=0)
                elif setting == "Rohtime" and str(eintrag.get("Rohtime")) <>  "None":
                    dynamic = True
                    time = eintrag.get("Rohtime")            
            for setting in eintrag:
                if setting == "offset" and str(eintrag.get("offset")) <>  "None":
                    time = time + datetime.timedelta(hours=0, minutes=int(eintrag.get("offset")), seconds=0)
                if setting == "Zufall" and str(eintrag.get("Zufall")) <>  "None":
                    time = time + datetime.timedelta(hours=0, minutes=random.randrange(int(eintrag.get("Zufall"))), seconds=0)                
            if dynamic:    
                with con:
                    #time = time - datetime.timedelta(seconds=int(str(time)[6:]))
                    cur = con.cursor()
                    sql = 'UPDATE '+constants.sql_tables.cron.name+' SET Time = "' + str(time) + '" WHERE Id = "'+ str(eintrag.get("Id")) + '"'
                    cur.execute(sql)
                con.close 
                
    def next_wecker_heute_morgen(self, horizont = 12):
        lt = localtime()
        Zeit = strftime("%H:%M", lt)
        tag = int(strftime("%w", lt))
        liste = self.get_next(tag, Zeit, wecker = True)
        if liste == []:
            text = "Kein Wecker fuer " + str(horizont) + " Stunden."
        else:
            text = "Wecker um " + str(liste[0].get("Time")).rsplit(':')[0] + " Uhr"
            if str(liste[0].get("Time")).rsplit(':')[1] <> "00":
                text = text + " " + str(liste[0].get("Time")).rsplit(':')[1]
            text = text + ", das ist in " + str(liste[0].get("delta")).rsplit(':')[0] + " Stunden"
            if str(liste[0].get("delta")).rsplit(':')[1] <> "00":
                text = text + " und " + str(liste[0].get("delta")).rsplit(':')[1] + " Minuten."
            else:
                text = text + "."
        #setting_s("Next_alarm", text)    
        return text                 

if __name__ == '__main__':
    main() 