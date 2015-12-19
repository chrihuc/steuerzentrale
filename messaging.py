#!/usr/bin/env python

import constants

from gcm import GCM
from mysql_con import setting_r, mdb_get_table# gcm_users_read
import time

def main():
    mes = messaging()
    constants.redundancy_.master = True
    print mes.send_direkt(to="Christoph", titel="Hinweis", text="test")
    
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
    
    def send_direkt(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(constants.sql_tables.Bewohner.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "Ein") and constants.redundancy_.master:
                    response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
                    if response <> {}:
                        success = False
        return success
        #response = self.gcm.json_request(registration_ids=to, data=data)

    def send_zuhause(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(constants.sql_tables.Bewohner.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "Ein") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('Name')) == "1"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)            
                        if response <> {}:
                            success = False
        return success
                        
    def send_abwesend(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = mdb_get_table(constants.sql_tables.Bewohner.name)
        for user in gcm_users:
            if user.get('Name') <> None:
                if (user.get('Name') in to) and (str(setting_r(str('Notify_'+ user.get('Name')))) == "Ein") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('Name')) == "0"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)                     
                        if response <> {}:
                            success = False
        return success
                        
    def send_wach(self, to, titel, text):
        if (setting_r("Status") != "Schlafen"):
            return self.send_direkt(to, titel, text)           


if __name__ == '__main__':
    main()