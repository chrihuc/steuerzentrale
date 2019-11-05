#!/usr/bin/env python

import constants

#from gcm import GCM
from database import mysql_connector as msqc
from outputs.mqtt_publish import mqtt_pub

import MySQLdb as mdb



table = constants.sql_tables.Bewohner

class Messaging:
    def __init__(self):
        #self.gcm = GCM(constants.gcm_ID)
        self.alle = []
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
        gcm_users = msqc.mdb_get_table(table.name)
        for user in gcm_users:
            if user.get('Name') != None:
                self.alle.append(user.get('Name'))

    def send_direkt(self, to, titel, text, prio=2):
        if not isinstance(to, list):
            if str(to) == 'Alle' or str(to) == 'None':
                to = self.alle
            elif isinstance(eval(to), list):  # eval('Christoph') gibt error
                to = eval(to)
            else:
                to = [to]        
        success = True
        data = {'titel': titel, 'message': text, 'prio':prio}
        for empf in to:
            mqtt_pub("Message/" + empf, data)
        return success
        #response = self.gcm.json_request(registration_ids=to, data=data)

    def send_zuhause(self, to, titel, text, prio=2):
        if not isinstance(to, list):
            if str(to) == 'Alle' or str(to) == 'None':
                to = self.alle
            elif isinstance(eval(to), list):
                to = eval(to)
            else:
                to = [to]
        success = True
        data = {'titel': titel, 'message': text, 'prio':prio}
        for empf in to:
            anw = msqc.setting_r(empf)
            if str(anw) == 'None':
                mqtt_pub("Message/" + empf, data)
            elif eval(anw):               
                mqtt_pub("Message/" + empf, data)            
        return success

#   deprecated
    def send_abwesend(self, to, titel, text, prio=2):
        if not isinstance(to, list):
            if str(to) == 'Alle' or str(to) == 'None':
                to = self.alle
            elif isinstance(eval(to), list):
                to = eval(to)
            else:
                to = [to]
        success = True
        data = {'titel': titel, 'message': text, 'prio':prio}
        for empf in to:
            anw = msqc.setting_r(empf)
            if not eval(anw):               
                mqtt_pub("Message/" + empf, data)            
        return success

#    deprecated
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
