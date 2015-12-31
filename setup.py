#!/usr/bin/env python

import constants

import MySQLdb as mdb 


def main():
    password = raw_input('Enter mysql root password: ')
    con = mdb.connect('localhost', 'root', password, '')
    with con:
        cur = con.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS "+ constants.sql_.DB+";"
        cur.execute(sql)
        results = cur.fetchall()
        print results   
        sql = "grant all on "+ constants.sql_.DB+".* to '" + constants.sql_.USER + "'@'%' identified by '" + constants.sql_.PASS + "'"
        cur.execute(sql)
        results = cur.fetchall()      
        print results
    con.close()
    con = mdb.connect('localhost', 'root', password, constants.sql_.DB)
    with con:    
        cur = con.cursor()
        for att in constants.sql_tables.tables:
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+att.name+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+att.name +"("
                for num, col in enumerate(att.columns):
                    if num == len(att.columns)-1:
                        for co in col:
                            command += co + " "
                        command +=  ");"
                    else:
                        for co in col:
                            command += co + " "                    
                        command +=  ", "
                print command
                cur.execute(command)
                results = cur.fetchall()      
                print results
        for att in constants.sql_tables.inps:
            for dev in att.columns:
                try:
                    query = "ALTER TABLE "+constants.sql_.DB+"."+constants.sql_tables.szenen.name+" ADD %s VARCHAR(20)" % (dev)
                    cur.execute( query )
                except:
                    pass
        cur.execute("SELECT COUNT(*) FROM "+constants.sql_.DB+"."+constants.sql_tables.szenen.name+" WHERE Name = 'Device_Type'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+constants.sql_tables.szenen.name+' (Id,Name) VALUES (1,"Device_Type")'  
            cur.execute(sql)
        for att in constants.sql_tables.inps:
            for dev in att.columns:
                sql = 'UPDATE '+constants.sql_tables.szenen.name+' SET '+dev+' = "' + att.name + '" WHERE Name = "Device_Type"'
                cur.execute(sql)
        cur.execute("SELECT COUNT(*) FROM "+constants.sql_.DB+"."+constants.sql_tables.szenen.name+" WHERE Name = 'Auto_Mode'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+constants.sql_tables.szenen.name+' (Id,Name) VALUES (2,"Auto_Mode")'  
            cur.execute(sql)
        for att in constants.sql_tables.inps:
            for dev in att.columns:
                sql = 'UPDATE '+constants.sql_tables.szenen.name+' SET '+dev+' = "auto" WHERE Name = "Auto_Mode"'
                cur.execute(sql)    
        cur.execute("SELECT COUNT(*) FROM "+constants.sql_.DB+"."+constants.sql_tables.szenen.name+" WHERE Name = 'Group'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+constants.sql_tables.szenen.name+' (Id,Name) VALUES (3,"Group")'  
            cur.execute(sql)     
        cur.execute("SELECT COUNT(*) FROM "+constants.sql_.DB+"."+constants.sql_tables.szenen.name+" WHERE Name = 'Value'")
        if cur.fetchone()[0] == 0:
            sql = 'INSERT INTO '+constants.sql_tables.szenen.name+' (Id,Name) VALUES (4,"Value")'  
            cur.execute(sql)              
    con.close()  


if __name__ == '__main__':
    main()    
    