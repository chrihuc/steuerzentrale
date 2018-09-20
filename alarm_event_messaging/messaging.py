#!/usr/bin/env python

import constants

#from gcm import GCM
from database import mysql_connector as msqc
from outputs.mqtt_publish import mqtt_pub

import MySQLdb as mdb
from outputs.mqtt_publish import mqtt_pub


table = constants.sql_tables.Bewohner

class Messaging:
    def __init__(self):
        #self.gcm = GCM(constants.gcm_ID)
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
        gcm_users = msqc.mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') != None:
                if (user.get('Name') in to) and constants.redundancy_.master:
#                    response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
                    mqtt_pub("Message/" + str(user.get('Name')), data)
#                    if response != {}:
#                        success = False
        return success
        #response = self.gcm.json_request(registration_ids=to, data=data)

    def send_zuhause(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = msqc.mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') != None:
                if (user.get('Name') in to) and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(msqc.setting_r(user.get('Name')) == "True"):
#                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
                        mqtt_pub("Message/" + str(user.get('Name')), data)
#                        if response != {}:
#                            success = False
        return success

    def send_abwesend(self, to, titel, text):
        success = True
        data = {'titel': titel, 'message': text}
        gcm_users = msqc.mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') != None:
                if (user.get('Name') in to) and constants.redundancy_.master:
                #if user.get('gcm_regid') in to:
                    if str(msqc.setting_r(user.get('Name')) == "False"):
                        mqtt_pub("Message/" + str(user.get('Name')), data)
#                        response = self.gcm.json_request(registration_ids=[user.get('gcm_regid')], data=data)
#                        if response != {}:
#                            success = False
        return success

    def send_wach(self, to, titel, text):
        if (msqc.setting_r("Status") != "Schlafen"):
            return self.send_direkt(to, titel, text)


    def register_user(self, user_desc):
        if user_desc['Name'] == '':
            return False
        found = False
        update = False
        gcm_users = msqc.mdb_get_table(table.name)
        for user in gcm_users:
            if user_desc['Name'] == user['Name']:
                found = True
                commands = {}
                if str(user_desc['Android_id']) != str(user['gcm_name']):
                    commands['gcm_name'] = user_desc['Android_id']
                    update = True
                if str(user_desc['Reg_id']) != str(user['gcm_regid']):
                    commands['gcm_regid'] = user_desc['Reg_id']
                    update = True
                if update:
                    msqc.mdb_set_table(table.name, user_desc['Name'], commands)
        if not found:
            commands = {}
            commands['gcm_name'] = user_desc['Android_id']
            commands['gcm_regid'] = user_desc['Reg_id']
            commands['Name'] = user_desc['Name']
            msqc.mdb_add_table_entry(table.name, commands)
        if update or not found:
            self.send_direkt(user_desc['Name'], 'Hinweise', 'User registered')
        return True
