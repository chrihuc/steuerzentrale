#!/usr/bin/env python

import constants 

import MySQLdb as mdb
import os


def main():
    ssync = sync()
    for table in ["Settings","Besucher","Bewohner","cron","gcm_users","Szenen","Wecker","Fern_Haupt","Fern_Flur","Fern_Esszi","Fern_Reduit","Fern_Schlafzi","Fern_Bad","Hue","hue_autolicht","KeyActions","LightstripSchlafzi","Marantz","satellites","Sideboard","Sonos","tc_abwesend","tc_am_gehen","tc_einer_wach","tc_gegangen","tc_immer","tc_schlafen","tc_schlafen_gehen","tc_schlummern","tc_status","tc_urlaub","tc_wach","tc_wecken","TuerSPi"]:
        ssync.export(table, "XS1DB", True)
        #ssync.trunc_import(table, "XS1DB") 


class sync:
    def __init__(self):
        self.user_r = "python_user"
        self.pass_r = "python"
        self.host_r = constants.redundancy_.partner_IP
        self.user_ = "customer"
        self.pass_ = "user"
        self.host_ = "localhost"       
        self.temp_f = constants.temp_folder
        self.temp_folder = "/home/pi/steuerzentrale/sql/"
    
    def export(self, table, db, for_git = False):
        #exectext = 'mysql -h '+self.host_r+' -u '+self.user_r+' --password='+self.pass_r+' -D '+db+' -e "SELECT * FROM '+table+'" > '+self.temp_f+table+'.sql'
        if for_git:
            exectext = 'mysqldump -h '+self.host_+' -u '+self.user_+' --password='+self.pass_+" "+db+' '+table+' > '+self.temp_folder+table+'.sql'
        else:
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