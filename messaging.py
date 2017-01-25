#!/usr/bin/env python

import constants

from gcm import GCM
from mysql_con import setting_r, mdb_get_table# gcm_users_read
import time
import MySQLdb as mdb

def main():
    mes = messaging()
    constants.redundancy_.master = True
#    print mes.send_direkt(to="Christoph", titel="Hinweis", text="test")
    print mes.send_direkt(to="Christoph", titel="Setting", text="Tag")
    
table = constants.sql_tables.Bewohner    
    
class messaging:
    def __init__(self):
        self.gcm = GCM(constants.gcm_ID)
        self.chris_vorname = "Christoph"
        self.sabina_vorname = "Sabina"
        self.chris = ['Christoph']
        self.sabina = ['Sabina'] 
        self.tf201 = ['tf201'] 
        self.alle = self.chris + self.sabina + self.tf201
        self.dict_namen = {self.chris[0]:self.chris_vorname, self.sabina[0]:self.sabina_vorname}
        self.__init_table__()
    
    def __init_table__(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+table.name+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+table.name +"("
                for num, col in enumerate(table.columns):
                    if num == len(table.columns)-1:
                        for co in col:
                            command += co + " "
                        command +=  ");"
                    else:
                        for co in col:
                            command += co + " "                    
                        command +=  ", "
                cur.execute(command)
                results = cur.fetchall()      
        con.close()     
    
    def send_direkt(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "True") and constants.redundancy_.master:
                    response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
                    print response
                    if response <> {}:
                        success = False
        return success
        #response = self.gcm.json_request(registration_ids=to, data=data)

    def send_zuhause(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "True") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('Name')) == "True"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)            
                        if response <> {}:
                            success = False
        return success
                        
    def send_abwesend(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "True") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('Name')) == "False"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)                     
                        if response <> {}:
                            success = False
        return success
                        
    def send_wach(self, to, titel, text):
        if (setting_r("Status") != "Schlafen"):
            return self.send_direkt(to, titel, text)           


if __name__ == '__main__':
    main()