#!  /usr/bin/python

import constants

import MySQLdb as mdb

def main():
    wohnT = temp_derivator("Wohnzimmer_T")
    RolAvg =  wohnT.get_avg("Value",13)
    wohnT.write_data("RolAvg",RolAvg)
    D60 = RolAvg - wohnT.get_hist_value("RolAvg",60)
    D30 = RolAvg - wohnT.get_hist_value("RolAvg",30)
    D15 = RolAvg - wohnT.get_hist_value("RolAvg",15)
    wohnT.write_data("D60",D60)
    wohnT.write_data("D30",D30)
    wohnT.write_data("D15",D15)
    
class temp_derivator:
    def __init__(self,db):
        self.data = []
        self.db = db
        
    def get_data(self,value,amount):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        list = []
        with con:
            cur = con.cursor()
            sql = 'SELECT '+value+' FROM '+self.db+' ORDER by Id DESC LIMIT '+str(amount)+';'
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            for row in results:
                for i in range (0,len(row)):
                   #print row[i]
                   list.append(row[i])          
            return list 
        con.close()
    
    def get_avg(self,value,amount):
        liste = self.get_data(value,amount)
        sum = 0
        count = 0
        for element in liste:
            sum += element
            count += 1
        if count > 0:
            return sum/count
        else:
            return 0
            
    def write_data(self,name,value):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'UPDATE '+self.db+' SET '+name+' = "' + str(value) + '" ORDER BY `id` DESC LIMIT 1'
            cur.execute(sql)
        con.close()        
        
    def get_hist_value(self,value,time):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            sql = 'SELECT '+value+' FROM '+self.db+' where Date > DATE_ADD(NOW(), INTERVAL -'+str(time)+' MINUTE) ORDER BY `id` LIMIT 1;'
            cur.execute(sql)
            results = cur.fetchall()
            field_names = [i[0] for i in cur.description]
            #dicti = {key: "" for (key) in szene_columns}
            for row in results:
                for i in range (0,len(row)):
                   #print row[i]
                   value = row[i]
            if str(value) == "None":
                value = 0
            return value 
        con.close()        
        
if __name__ == '__main__':
    main()        