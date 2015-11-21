#!/usr/bin/env python

import constants

import MySQLdb as mdb 


def main():
    con = mdb.connect('localhost', 'root', 'Ivenhoe', '')
    with con:
        cur = con.cursor()
        sql = "grant all on *.* to '" + constants.sql_.USER + "'@'%' identified by '" + constants.sql_.PASS + "'"
        cur.execute(sql)
        results = cur.fetchall()
        print results
        sql = "CREATE DATABASE IF NOT EXISTS "+ constants.sql_.DB+";"
        cur.execute(sql)
        results = cur.fetchall()
        print results        
    con.close()  


if __name__ == '__main__':
    main()    
    