#!/usr/bin/env python
"""
Created on Fri Sep 15 19:52:27 2016

@author: Christoph Huckle
"""

# pylint: disable=R0903
# pylint: disable=W0105
# pylint: disable=W0104
# pylint: disable=F0401

from time import localtime, strftime
import datetime
import random

import constants
from tools import decorators
from database.mysql_connector import mdb_get_table

import MySQLdb as mdb
import ephem

# TODO Tests

HOME = ephem.Observer()
HOME.lon = str(8.141716)
HOME.lat = str(47.438517)
HOME.elev = 400

class Cron(object):
    """ This class is reaging and updating timed events
    """
    def __init__(self):
        self.tage = {1:"Mo", 2:"Di", 3:"Mi", 4:"Do", 5:"Fr", 6:"Sa", 0:"So"}

    @staticmethod
    def get_now(tag, zeit, datab=constants.sql_tables.cron.name):
        """ returns a list of stored events wich are due now
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
        dicti = {}
        tage = {1:"Mo", 2:"Di", 3:"Mi", 4:"Do", 5:"Fr", 6:"Sa", 0:"So"}
        liste = []
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM %s WHERE %s="True" AND Time = "%s" AND Eingeschaltet="True"' % (datab, tage.get(tag), zeit)
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            j = 0
            for row in results:
                for i in range(0, len(row)):
                    dicti[field_names[i]] = row[i]
                liste.append(dicti)
                dicti = {}
                j = j + 1
        con.close
        return liste

    @staticmethod
    def get_all(wecker=False, typ=None):
        """ returns a list of stored events
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
        dicti = {}
        liste = []
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM '+constants.sql_tables.cron.name
            if wecker:
                sql = 'SELECT * FROM '+constants.sql_tables.cron.name+ ' WHERE Type ="Wecker"'
            if typ != None:
                sql = 'SELECT * FROM '+constants.sql_tables.cron.name+ ' WHERE Type ="'+typ+'"'
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            j = 0
            for row in results:
                for i in range(0, len(row)):
                    dicti[field_names[i]] = row[i]
                liste.append(dicti)
                dicti = {}
                j = j + 1
        con.close
        return liste

    def get_next(self, tag, zeit, wecker=False, datum=None):
        """ returns a list of stored events which are due next
            propose to load as pandas dataframe
        """
        liste = self.get_all(wecker=wecker)
        ret_item = {}
        ret_liste = []
        zeit = datetime.timedelta(hours=int(zeit[:zeit.find(":")]),
                                  minutes=int(zeit[zeit.find(":")+1:]), seconds=0)
        next_one = datetime.timedelta(hours=12, minutes=0, seconds=0)
        nulltime = datetime.timedelta(hours=0, minutes=0, seconds=0)
        morgen = tag + 1
        if morgen == 7:
            morgen = 0
        for eintrag in liste:
            if str(eintrag.get("Eingeschaltet")) <> "True":
                continue
#            if datab == "Wecker":
#                time = eintrag.get("Time") - eintrag.get("Offset")
#            else:
            time = eintrag.get("Time")
            if datum is None:
                datumscheck = True
            else:
                datumscheck = True
                if eintrag['Start'] != None:
                    thres_date = eintrag['Start']
                    if thres_date.year == 1111:
                        thres_date = datetime.datetime(datum.year, thres_date.month, thres_date.day)
                        if datum < thres_date:
                            datumscheck = False
                    else:
                        if datum < thres_date:
                            datumscheck = False
                if eintrag['End'] is not None:
                    thres_date = eintrag['End']
                    if thres_date.year == 1111:
                        thres_date = datetime.datetime(datum.year, thres_date.month,
                                                       thres_date.day) + datetime.timedelta(days=1)
                        if datum > thres_date:
                            datumscheck = False
                    else:
                        if datum < thres_date:
                            datumscheck = False
            if (str(eintrag.get(self.tage.get(tag))) == "True") and datumscheck:
                if ((time - zeit) == next_one) and (time - zeit) >= nulltime:
                    ret_item = eintrag
                    next_one = (time - zeit)
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)
                elif ((time - zeit) < next_one) and (time - zeit) >= nulltime:
                    ret_liste = []
                    ret_item = eintrag
                    next_one = (time - zeit)
                    ret_item["delta"] = next_one
                    ret_liste.append(ret_item)
            if (str(eintrag.get(self.tage.get(morgen))) == "True") and datumscheck:
                deltati = (time - zeit) + datetime.timedelta(hours=24, minutes=0, seconds=0)
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

    def get_now2(self, tag, zeit, date=None):
        """ returns a list of stored events which are due next
        """
        if date is None:
            now = datetime.datetime.now()
        liste = self.get_next(tag, zeit, False, now)
        if liste:
            if liste[0].get("delta") < datetime.timedelta(hours=0, minutes=1, seconds=0):
                return liste
        return []

    @decorators.deprecated
    def delete(ident):
        """ deletes the stored timed event, should not be used anymore
            use executed
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'DELETE FROM '+constants.sql_tables.cron.name+' WHERE id = '+ str(ident)
            cur.execute(sql)
        con.close()

    @staticmethod
    def executed(ident):
        """ sets the scheduled event to not active
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = ('UPDATE %s SET Eingeschaltet = "False" WHERE id = %s' %
                   (constants.sql_tables.cron.name, str(ident)))
            cur.execute(sql)
        con.close()

    @staticmethod
    def new_event(szene, time, bedingung="", permanent=0):
        """ creates a new scheduled event
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
        with con:
            cur = con.cursor()
            value_string = '"%s", "%s", "%s", "%s"' % (szene, str(time), str(bedingung),
                                                       str(permanent))
            insertstatement = ('INSERT INTO %s (Szene, Time, Bedingung, permanent) VALUES(%s)' %
                               (constants.sql_tables.cron.name, value_string))
            cur.execute(insertstatement)
        con.close

    @staticmethod
    def calculate():
        """ recalculates the trigger time, this is calculating random times
            and sunrise sunset times
        """
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS,
                          constants.sql_.DB)
#        dicti = {}
        liste = mdb_get_table(constants.sql_tables.cron.name)
#        with con:
#            cur = con.cursor()
#            sql = 'SELECT * FROM '+constants.sql_tables.cron.name
#            cur.execute(sql)
#            results = cur.fetchall()
#            field_names = [i[0] for i in cur.description]
#            j = 0
#            for row in results:
#                for i in range(0, len(row)):
#                    dicti[field_names[i]] = row[i]
#                liste.append(dicti)
#                dicti = {}
#                j = j + 1
#        con.close
        time = localtime()
        HOME.date = strftime("%Y-%m-%d 00:00:00", time)
        # check for daylight saving
        if getattr(localtime(), 'tm_isdst') > 0:
            delta = 2
        else:
            delta = 1
        sunrise = ((HOME.next_rising(ephem.Sun())).datetime() +
                   datetime.timedelta(hours=delta, minutes=0, seconds=0))
        sunset = ((HOME.next_setting(ephem.Sun())).datetime() +
                  datetime.timedelta(hours=delta, minutes=0, seconds=0))
        for eintrag in liste:
            dynamic = False
            for setting in eintrag:
                if setting == "Sonne" and str(eintrag.get("Sonne")) <> "None":
                    dynamic = True
                    if str(eintrag.get("Sonne")) == "rise":
                        time = sunrise.replace(second=0)
                    else:
                        time = sunset.replace(second=0)
                elif setting == "Rohtime" and str(eintrag.get("Rohtime")) <> "None":
                    dynamic = True
                    time = eintrag.get("Rohtime")
            for setting in eintrag:
                if setting == "offset" and str(eintrag.get("offset")) <> "None":
                    time = time + datetime.timedelta(hours=0, minutes=int(eintrag.get("offset")),
                                                     seconds=0)
                if setting == "Zufall" and str(eintrag.get("Zufall")) <> "None":
                    time = (time +
                            datetime.timedelta(hours=0,
                                               minutes=random.randrange(int(eintrag.get("Zufall"))),
                                               seconds=0))
            if dynamic:
                with con:
                    #time = time - datetime.timedelta(seconds=int(str(time)[6:]))
                    cur = con.cursor()
                    sql = ('UPDATE %s SET Time = "%s" WHERE Id = "%s"'
                           % (constants.sql_tables.cron.name, str(time), str(eintrag.get("Id"))))
                    cur.execute(sql)
                con.close
        return True

    def next_wecker_heute_morgen(self, horizont=12):
        """ calculates the time till the next alarm today or tomorrow
        """
        time = localtime()
        zeit = strftime("%H:%M", time)
        tag = int(strftime("%w", time))
        liste = self.get_next(tag, zeit, wecker=True)
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
