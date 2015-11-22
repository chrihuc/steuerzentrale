#!/usr/bin/env python

import constants

import MySQLdb as mdb
from mysql_con import setting_r

def main():
    tc = tablecontrol()
    print tc.get_szene(sensor = "Temperatur_Balkon", value = 2)

class tablecontrol:
    def __init__(self):
        self.a = 10
    
    def get_mysql_data(self, table, name):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM ' + str(table) +' WHERE tc_value = "' + str(name) +'"'
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            for row in results:
                for i in range (0,len(row)):
                   #print row[i]
                   dicti[field_names[i]] = row[i]            
        con.close
        return dicti        
        
    def get_status(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'SELECT * FROM Settings WHERE Name = "Status"'
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                fname = row[1]
                value = row[2]
                return value
        con.close    
        
    def get_table(self, status):
        return self.get_mysql_data(table = "tc_status", name = status).get("tc_table")
        
    def get_szene_alt(self, sensor, value):
        status  = self.get_status()
        table = self.get_mysql_data(table = "tc_status", name = status).get("tc_table")
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        szenen = []
        try:
            with con:
                cur = con.cursor()
                sql = 'SELECT * FROM ' + str(table) +' WHERE tc_sensor = "' + str(sensor) +'"'
                sql = sql + ' AND tc_enabled = "1"'
                value = str(value)
                sql = sql + ' AND ((tc_value_lt > "' + value + '" OR tc_value_lt is NULL )'
                sql = sql + ' AND (tc_value_eq = "' + value  + '" OR tc_value_eq is NULL )'
                sql = sql + ' AND (tc_value_gt < "' + value  + '" OR tc_value_gt is NULL )'
                sql = sql + ');'
                #SELECT * FROM XS1DB.tc_wach WHERE tc_sensor = "test" AND tc_enabled = "1" AND (tc_value_lt > "5" or tc_value_eq = "5" or tc_value_gt < "5");
                cur.execute(sql)
                results = cur.fetchall()
                field_names = [i[0] for i in cur.description]
                #dicti = {key: "" for (key) in szene_columns}
                for row in results:
                    for i in range (0,len(row)):
                       #print row[i]
                       dicti[field_names[i]] = row[i]  
                    szenen.append(dicti.get("tc_szene"))
            con.close
            with con:
                cur = con.cursor()
                sql = 'SELECT * FROM tc_immer WHERE tc_sensor = "' + str(sensor) +'"'
                sql = sql + ' AND tc_enabled = "1"'
                value = str(value)
                sql = sql + ' AND ((tc_value_lt > "' + value + '" OR tc_value_lt is NULL )'
                sql = sql + ' AND (tc_value_eq = "' + value  + '" OR tc_value_eq is NULL )'
                sql = sql + ' AND (tc_value_gt < "' + value  + '" OR tc_value_gt is NULL )'
                sql = sql + ');'
                #SELECT * FROM XS1DB.tc_wach WHERE tc_sensor = "test" AND tc_enabled = "1" AND (tc_value_lt > "5" or tc_value_eq = "5" or tc_value_gt < "5");
                cur.execute(sql)
                results = cur.fetchall()
                field_names = [i[0] for i in cur.description]
                #dicti = {key: "" for (key) in szene_columns}
                for row in results:
                    for i in range (0,len(row)):
                       #print row[i]
                       dicti[field_names[i]] = row[i]  
                    szenen.append(dicti.get("tc_szene"))
            con.close            
            return szenen 
        except mdb.ProgrammingError, e:
            return []
        
    def get_szene(self, sensor, value):
        status  = self.get_status()
        table = self.get_mysql_data(table = "tc_status", name = status).get("tc_table")
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        dicti = {}
        szenen = []
        tables = ['tc_immer']
        tables.append(table)
        try:
            for table in tables:
                with con:
                    cur = con.cursor()
                    sql = 'SELECT * FROM ' + str(table) +' WHERE tc_sensor = "' + str(sensor) +'"'
                    sql = sql + ' AND tc_enabled = "1";'
                    #SELECT * FROM XS1DB.tc_wach WHERE tc_sensor = "test" AND tc_enabled = "1" AND (tc_value_lt > "5" or tc_value_eq = "5" or tc_value_gt < "5");
                    cur.execute(sql)
                    results = cur.fetchall()
                    field_names = [i[0] for i in cur.description]
                    #dicti = {key: "" for (key) in szene_columns}
                    for row in results:
                        bedingung1 = True
                        bedingung2 = True
                        bedingung3 = True
                        for i in range (0,len(row)):
                            dicti[field_names[i]] = row[i]  
                        schwelle_ob = dicti.get("tc_value_gt")
                        if schwelle_ob is not None:
                            try:
                                schwelle_ob = eval(schwelle_ob)
                            except NameError:
                                schwelle_ob = setting_r(str(schwelle_ob))  
                            except TypeError:
                                pass                        
                            if (float(value) > float(schwelle_ob)):
                                bedingung1 = True
                            else:
                                bedingung1 = False
                        schwelle_un = dicti.get("tc_value_lt")
                        if schwelle_un is not None:
                            try:
                                schwelle_un= eval(schwelle_un)
                            except NameError:
                                schwelle_un = setting_r(str(schwelle_un)) 
                            except TypeError:
                                pass                        
                            if (float(value) < float(schwelle_un)):
                                bedingung2 = True 
                            else:
                                bedingung2 = False                            
                        schwelle_gl = dicti.get("tc_value_eq")  
                        if schwelle_gl is not None:
                            #print schwelle_gl
                            try:
                                schwelle_gl = eval(schwelle_gl)
                            except NameError:
                                schwelle_gl = setting_r(str(schwelle_gl))
                            except TypeError:
                                pass
                            if (float(value) == float(schwelle_gl)):
                                bedingung3 = True 
                            else:
                                bedingung3 = False                            
                        if bedingung1 and bedingung2 and bedingung3:
                            szenen.append(dicti.get("tc_szene"))                        
                con.close           
            return szenen 
        except mdb.ProgrammingError, e:
            return []      
        
if __name__ == '__main__':
    main()         