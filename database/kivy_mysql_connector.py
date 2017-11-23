#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:08:21 2017

@author: christoph

Module to allow the kivy guy connect to the database and retrieve all
neccessary information
"""

import constants

import MySQLdb as mdb


#kompletter table:
def get_table(table):
    con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
    rlist = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM %s' % (table)
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti = {}
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]  
            rlist.append(dicti)
    con.close()    
    return rlist 


def list_scenes(typ=None):
    scn_table = get_table(constants.sql_tables.szenen.name)
    if typ is None:
        scn_list = [entry['Name'] for entry in scn_table]
    elif isinstance(typ,list):
        scn_list = [entry['Name'] for entry in scn_table if entry['Gruppe'] in typ]
    else:
        scn_list = [entry['Name'] for entry in scn_table if entry['Gruppe'] == typ]
    return scn_list