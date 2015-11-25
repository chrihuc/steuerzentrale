#!/usr/bin/env python

import constants

from gcm import GCM
from mysql_con import setting_r, gcm_users_read
import time

def main():
    mes = messaging()
    print mes.send_direkt(to="Christoph", titel="Hinweis", text="test")
    
class messaging:
    def __init__(self):
        self.gcm = GCM(constants.gcm_ID)
        self.chris_vorname = "Christoph"
        self.sabina_vorname = "Sabina"
        #self.chris = ['APA91bFDedZormESEhuUTQMm_GIrb66WcPVfymg652VAvXlnO82deVgW1KzrpJbcVUlhz69lXAyhRBeMDg8SOfGSkLK9UVKgPRN9IeWIsAqCMFpgMCYcbONU_xKonRJKL4tLdHxtu7J7m6JNmibTsH0g8NUCgoM-vQ']
        #self.sabina = ['APA91bGqnxqMZSspTmBbSgUvcqXE6fojwJOptq1dmt1tieocrc0HXqnS54CVOX4oMFdDOAdz-l1C_U1YPrzr6VHSnGg3cw9s1OjsXWcf_O4N1pdDIwAK_elPDNArR-v2QNKPrlkwWBqlQGDS6yIJ2I0qxAXVuWzQcw']
        self.chris = ['Christoph']
        self.sabina = ['Sabina'] 
        self.tf201 = ['tf201'] 
        self.alle = self.chris + self.sabina + self.tf201
        self.dict_namen = {self.chris[0]:self.chris_vorname, self.sabina[0]:self.sabina_vorname}
    
    def send_direkt(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = gcm_users_read()
        for user in gcm_users:
            if user.get('vorname') <> None:
                if (user.get('vorname') in to) and (str(setting_r(str('Notify_'+ user.get('vorname')))) == "Ein") and constants.redundancy_.master:
                    response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
                    if response <> {}:
                        success = False
        return success
        #response = self.gcm.json_request(registration_ids=to, data=data)

    def send_zuhause(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = gcm_users_read()
        for user in gcm_users:
            if user.get('vorname') <> None:
                if (user.get('vorname') in to) and (str(setting_r(str('Notify_'+ user.get('vorname')))) == "Ein") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('vorname')) == "1"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)            
                        if response <> {}:
                            success = False
        return success
                        
    def send_abwesend(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = gcm_users_read()
        for user in gcm_users:
            if user.get('vorname') <> None:
                if (user.get('vorname') in to) and (str(setting_r(str('Notify_'+ user.get('vorname')))) == "Ein") and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(setting_r(user.get('vorname')) == "0"):
                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)                     
                        if response <> {}:
                            success = False
        return success
                        
    def send_wach(self, to, titel, text):
        if (setting_r("Status") != "Schlafen"):
            return self.send_direkt(to, titel, text)           

#gcm.plaintext_request(registration_id=reg_id_c, data=data)
if __name__ == '__main__':
    main()