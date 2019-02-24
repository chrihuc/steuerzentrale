# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:58:42 2016

@author: chuckle
"""

#import socket

import os
import time, datetime
import glob
#from subprocess import call

import constants
import git
import requests
from alarm_event_messaging import alarmevents

#from database import mysql_connector
from outputs import simulation
from tools import toolbox

# TODO Tests split adress from hks

#HOST = constants.udp_.SERVER   # Symbolic name meaning the local host
#PORT = constants.udp_.biPORT    # Arbitrary non-privileged port
aes = alarmevents.AES()

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
    toolbox.communication.send_message(payload, typ='InputValue')
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.settimeout(10)
#    try:
#        s.connect((HOST,PORT))
#        s.send(str(message))
#        reply = s.recv(1024)
#    finally:
#        s.close()
#    if str(reply) == str(message):
#        return True
#    return False

        
def check_ext_ip():
    ip = requests.get('https://api.ipify.org').text
    if ip != constants.ext_IP:
        constants.ext_IP = ip
        aes.new_event(description="New IP "+ip, prio=8)
        constants.config.set('Main', 'Ext_IP', ip)
        constants.save_config()
    else:
        pass
#            aes.new_event(description="Old IP "+ip, prio=8)

class Internal:

    def __init__ (self):
        dev_list = {'V00ESS1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0),
                                       datetime.time(22, 30, 0, 0), 30, 20, 50),
                    'V00KUE1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0),
                                       datetime.time(22, 30, 0, 0), 30, 1, 10),
                    'V00KUE1DEK1LI02':('On', 'Off', datetime.time(7, 0, 0, 0),
                                       datetime.time(22, 30, 0, 0), 30, 1, 10),
                    'V00FLU1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                                       datetime.time(22, 30, 0, 0), 30, 1, 30),
                    'V01FLU1DEK1LI01':('On', 'Off', datetime.time(7, 0, 0, 0), 
                                       datetime.time(22, 30, 0, 0), 30, 1, 30),
                    'V00WOH1RUM1LI13':('Ambience', 'Aus', datetime.time(7, 0, 0, 0), 
                                       datetime.time(23, 0, 0, 0), 30, 50, 25)}
        min_off_dict = {'V00ESS1DEK1LI01':20,
                        'V00KUE1DEK1LI01':10,
                        'V00KUE1DEK1LI02':10,
                        'V00FLU1DEK1LI01':45,
                        'V01FLU1DEK1LI01':30,
                        'V00WOH1RUM1LI13':5}
        min_on_dict = {'V00ESS1DEK1LI01':10,
                       'V00KUE1DEK1LI01':1,
                       'V00KUE1DEK1LI02':1,
                       'V00FLU1DEK1LI01':0,
                       'V01FLU1DEK1LI01':0,
                       'V00WOH1RUM1LI13':20}
        increments = ['V00KUE1DEK1LI01',
                      'V00KUE1DEK1LI02',
                      'V00FLU1DEK1LI01',
                      'V01FLU1DEK1LI01']
        self.ghost = simulation.anwesenheits_geist(dev_list)
        self.ghost.set_latches(min_off_dict, min_on_dict)
        self.ghost.set_increments(increments)
        pass

    def list_commands(self):
        return ['Restart','Update', 'Check_Anwesenheit', 'convert_mts', 'Klingel_Mail',
                'geist_start', 'geist_stop', 'check_ext_ip']

    def execute(self, commd):
        if commd == 'Update':
            self.git_update()
        elif commd == 'Check_Anwesenheit':
            self.check_anwesenheit()
        elif commd == 'convert_mts':
            self.convert_mts()
        elif commd == 'geist_start':
            self.zeitgheist_start()
        elif commd == 'geist_stop':
            self.zeitgheist_stop()
        elif commd == 'Klingel_Mail':
            aes.send_mail('Klingel', text='', url='http://192.168.192.36/html/cam.jpg')
        elif commd == 'Restart':
            self.restart()
        elif commd == 'check_ext_ip':
            check_ext_ip()            

    def restart(self):
        constants.run = False
        aes.new_event(description="Restarting in 60", prio=7)
        time.sleep(60)
#        sys.exit("XS1 goodbye")
        exectext = "sudo killall python3"
        aes.new_event(description="Restarting", prio=7)
        os.system(exectext)        

    def git_update(self):
        g = git.cmd.Git()
        g.reset('--hard')
        g.pull()

        print("Update done, exiting")
        aes.new_event(description="Update performed, restarting", prio=1)
        constants.run = False

    def check_anwesenheit(self):
#        bewohner = mysql_connector.mdb_get_table(constants.sql_tables.Bewohner.name)
#        alle_da = True
#        alle_weg = True
#        alle_da_act = eval(mysql_connector.setting_r('Alle_Bewohner_anwesend'))
#        alle_weg_act = eval(mysql_connector.setting_r('Alle_Bewohner_abwesend'))
#        for person in bewohner:
#            anwesend = False
#            ip_adress = person['Handy_IP']
#            if ip_adress == None:
#                continue
#            state = person['Handy_State']
#            if state == None:
#                state = 0
#            else:
#                state = int(state)
#            if toolbox.ping(ip_adress):
#                person['Handy_State'] = 5
#                anwesend = True
#            else:
#                person['Handy_State'] = state - 1
#            cmd = {'Handy_State':person['Handy_State']}
#            mysql_connector.mdb_set_table(constants.sql_tables.Bewohner.name, person['Name'], cmd)  
#            broadcast_input_value('Bewohner.'+person['Name']+'.Handy', int(state))
#            TODO: Table anpassend und Zeilen einkommentieren
#            akt_state_usb = eval(mysql_connector.setting_r(person['HKS_USB']))
#            if akt_state_usb == 1:
#                anwesend = True
#            broadcast_input_value('Bewohner.'+person['Name']+'.Anwesend', int(anwesend))
            
#            name = 'Bew_' + str(person['Name'])
#            akt_stat = eval(mysql_connector.setting_r(person['Name']))
#            if state == None:
#                state = 0
#            else:
#                state = int(state)
#                if state > 1:
#                    new_state = True
#                elif state < 2:
#                    new_state = False
#            alle_da = alle_da & new_state
#            alle_weg = alle_weg & (not new_state)
#            if akt_stat != new_state:
#                mysql_connector.setting_s(person['Name'], new_state)
#                broadcast_input_value(name, int(new_state))

#        if alle_da_act != alle_da:
#            mysql_connector.setting_s('Alle_Bewohner_anwesend', alle_da)
#            broadcast_input_value('Bew_alle_da', int(alle_da))
#
#        if alle_weg_act != alle_weg:
#            mysql_connector.setting_s('Alle_Bewohner_abwesend', alle_weg)
#            broadcast_input_value('Bew_alle_weg', int(alle_weg))

        return True


    def convert_mts(self):
        for dirname, dirnames, filenames in os.walk('/mnt/array1/photos/2017'):
            for subdirname in dirnames:
                folder = os.path.join(dirname, subdirname)
                for filename in glob.glob(os.path.join(folder, '*.MTS')):
                    if True: #not os.path.isfile(filename[:-3]+'MP4'):
                        cmd = 'ffmpeg -i "' + filename + '" -s 800x450 -c:a aac -q:a 2 -b:v 1000k -strict experimental "' + filename[:-3]+'MP4"'
                        os.system(cmd)
                        os.chmod(filename[:-3]+'MP4', 777)

    def zeitgheist_start(self):
        self.ghost.start()

    def zeitgheist_stop(self):
        self.ghost.stop()
