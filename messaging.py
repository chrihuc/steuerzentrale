#!/usr/bin/env python

import constants

from gcm import GCM
from mysql_con import setting_r, mdb_get_table, mdb_set_table, mdb_add_table_entry# gcm_users_read
import time
import MySQLdb as mdb

def main():
    mes = messaging()
    constants.redundancy_.master = True
#    print mes.send_direkt(to="Christoph", titel="Hinweis", text="test")
#    print mes.send_direkt(to="Christoph", titel="Setting", text="Tag")
    print mes.register_user({'Android_id':'413cf24a528eb3e3', 'Name':'Christoph',
                             'Reg_id':'APA91bFX8yBcE6FDPT7zA1tfNq55wQa6H4OH9DfRAILxNEnUs1Lds5jjqVEselR6pu-8TjfmODquvOe27ujiIw68OdO7lHpy2hn3mvOUkqFGqU6HvZyLhElpcKuPc5cZfI3X--9kBGP3IMsgRThkbA-7FEQz4TifYg'})
    
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

            
    def register_user(self, user_desc):
        if user_desc['Name'] == '':
            return False
        found = False
        update = False
        gcm_users = mdb_get_table(table.name)
        for user in gcm_users:
            if user_desc['Name'] == user['Name']:
                found = True
                commands = {}
                if str(user_desc['Android_id']) <> str(user['gcm_name']):
                    commands['gcm_name'] = user_desc['Android_id']
                    update = True
                if str(user_desc['Reg_id']) <> str(user['gcm_regid']):
                    commands['gcm_regid'] = user_desc['Reg_id']
                    update = True                    
                if update:
                    mdb_set_table(table.name, user_desc['Name'], commands)
        if not found:
            commands = {}
            commands['gcm_name'] = user_desc['Android_id']
            commands['gcm_regid'] = user_desc['Reg_id']
            commands['Name'] = user_desc['Name']
            mdb_add_table_entry(table.name, commands)
        if update or not found:
            self.send_direkt(user_desc['Name'], 'Hinweise', 'User registered')
        return True

if __name__ == '__main__':
    main()