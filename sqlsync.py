#!/usr/bin/env python

import constants 

import MySQLdb as mdb
import os

def main():
    ssync = sync()
    for table in ["Settings","Besucher","Bewohner","cron","gcm_users","Szenen","Wecker"]:
        ssync.export(table, "XS1DB")
        ssync.trunc_import(table, "XS1DB") 


class sync:
    def __init__(self):
        self.user_r = "python_user"
        self.pass_r = "python"
        self.host_r = constants.redundancy_.partner_IP
        self.temp_f = constants.temp_folder
    
    def export(self, table, db):
        exectext = 'mysql -h '+self.host_r+' -u '+self.user_r+' --password='+self.pass_r+' -D '+db+' -e "SELECT * FROM '+table+'" > '+self.temp_f+table+'.sql'
        exectext = 'mysqldump -h '+self.host_r+' -u '+self.user_r+' --password='+self.pass_r+" "+db+' '+table+' > '+self.temp_f+table+'.sql'
        #print exectext
        os.system(exectext) 
    
    def trunc_import(self, table, db):
        #con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        #with con:
            #cur = con.cursor()
            #sql = 'TRUNCATE TABLE ' + table 
            #cur.execute(sql)
            #sql = 'LOAD DATA LOCAL INFILE "'+self.temp_f+table+'.sql'+'" REPLACE INTO TABLE '+db+'.'+table+' IGNORE 1 LINES'
            #cur.execute(sql)
        #con.close()
        exectext = 'mysql -u '+constants.sql_.USER+' --password='+constants.sql_.PASS+' '+constants.sql_.DB+'< '+self.temp_f+table+'.sql'
        os.system(exectext) 
        
if __name__ == '__main__':
    main()        