# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:36:06 2019

@author: hc
"""

import time

import constants
from tools import toolbox
from alarm_event_messaging import alarmevents as aevs
from database import mysql_connector as msqc
aes = aevs.AES()


from secvest.secvest import Secvest

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value, level=9)
    toolbox.communication.send_message(payload, typ='InputValue')

class SecvestHandler(object):
    
    def __init__(self):
        self.commandActive = False
        self.checkActive= False
        self.cycleTime = 15
        self.alarmanlage = None
        self.alarms = []
        self.faults = {}


    def activate(self, alarmanlage, partition=1):
        alarmanlage.set_partition(partition)
    #    check
        success = False
        status_part = alarmanlage.get_partition(partition)
        if status_part['state'] == 'set':
#            print('ok')
            aes.new_event(description="Secvest aktiv", prio=0)
            broadcast_input_value('Secvest.Partition' + str(partition), str(1))
            success = True
        else:
#            aes.new_event(description="Secvest konnte nicht aktiviert werden", prio=9)
            self.__check_zones__(partition, hinweis=True)
            print('Konnte die Partition nicht aktivieren')
            payload = {'Szene':'SecvestInfo', 'desc':'Secvest konnte nicht aktiviert werden'}
            toolbox.communication.send_message(payload, typ='ExecSzene')             
        return success
    
    def deactivate(self, alarmanlage, partition=1):
        alarmanlage.unset_partition(partition)
    #    check
        success = False
        status_part = alarmanlage.get_partition(partition)
        if status_part['state'] == 'unset':
#            print('ok')
            aes.new_event(description="Secvest deaktiviert", prio=0)
            broadcast_input_value('Secvest.Partition' + str(partition), str(0))
            success = True
        else:
            print('Konnte die Partition nicht deaktivieren')
#            aes.new_event(description="Secvest konnte nicht deaktiviert werden", prio=9)
            payload = {'Szene':'SecvestInfo', 'desc':'Secvest konnte nicht deaktiviert werden'}
            toolbox.communication.send_message(payload, typ='ExecSzene')               
        return success    
        
    def __check_zones__(self, partition=1, hinweis=False):
        zonen = self.alarmanlage.get_zones_by_partition(partition)
        for zone in zonen:
            if zone['state'] != 'closed':
                broadcast_input_value('Secvest.Partition' + str(partition) + '.' + zone['name'], str(1))
                if hinweis:
#                    aes.new_event(description=zone['name'] + ' ist nicht geschlossen', prio=6)
                    payload = {'Szene':'SecvestInfo', 'desc':zone['name'] + ' ist nicht geschlossen'}
                    toolbox.communication.send_message(payload, typ='ExecSzene')                     
            else:
                broadcast_input_value('Secvest.Partition' + str(partition) + '.' + zone['name'], str(0))            
        
    def check_ob_zu(self, partition=None):
        if partition is None:
            for partition in range(1,5):
                self.__check_zones__(partition)
        else:
            self.__check_zones__(partition)        
        result = True
        return result
    
    def get_faults(self):
        faults = self.alarmanlage.get_faults() 
        for fault in faults:
#            {'type': '5000', 'id': '1474', 'ui-string': 'Z201 A Terrassentür', 'affects-partition': ['1'], 'affects-zone': '201', 'prevents-set': True, 'prevents-reset': False, 'is-rf-warning': False}
            if not fault['ui-string'] in self.faults:
#                print(fault)
                if fault['is-rf-warning']:
                    payload = {'Szene':'SecvestDebug', 'desc':'Warnung: ' + fault['ui-string']}
                    toolbox.communication.send_message(payload, typ='ExecSzene')
                self.faults[fault['ui-string']] = fault
        delete = []
        for stored,value in self.faults.items():
            found = False
            for fault in faults:
                if stored == fault['ui-string']:
                    found = True
            if not found and value['is-rf-warning']: 
                payload = {'Szene':'SecvestDebug', 'desc':'Ok: ' + value['ui-string']}
                toolbox.communication.send_message(payload, typ='ExecSzene') 
                delete.append(stored)
        for item in delete:
            self.faults.pop(item, True)                            
        result = True
        return result 
    
    def get_alarms(self):
#        {'id': '65537', 'type': '1', 'affects-partition': '1'}   1 oder 4 sabotage gehäuse 
#        {'id': '65540', 'type': '4', 'affects-partition': '1'}   4 ist scheinbar Sabotage

        alarms = self.alarmanlage.get_alarms() 
        for alarm in alarms:
            if not alarm in self.alarms:
                if alarm['type'] == '1':
                    payload = {'Szene':'SecvestInfo', 'desc':'Einbruch'}
                if alarm['type'] == '4':
                    payload = {'Szene':'SecvestInfo', 'desc':'Sabotage'}                    
                toolbox.communication.send_message(payload, typ='ExecSzene')
                self.alarms.append(alarm)
            if not alarm['type'] in ['1', '4']:
                print(alarm)
        delete = []                
        for alarm in self.alarms:
            if not alarm in alarms:
                if alarm['type'] == '1':
                    payload = {'Szene':'SecvestInfo', 'desc':'Einbruch'+ ' wieder weg.'}
                if alarm['type'] == '4':
                    payload = {'Szene':'SecvestInfo', 'desc':'Sabotage'+ ' wieder weg.'}                   
#                payload = {'Szene':'SecvestInfo', 'desc':alarm + ' wieder weg.'}
                toolbox.communication.send_message(payload, typ='ExecSzene')
                delete.append(alarm)
        for item in delete:
            self.alarms.pop(item, True)                              
        result = True
        return result    
    
    def set_device(self, command, partition, *args,**kwargs):
        try:
            #alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
            result = False
            self.commandActive = True
            while self.checkActive:
                time.sleep(1)            
            if command == 'activate':
                result = self.activate(self.alarmanlage, partition)
            elif command == 'deactivate':
                result = self.deactivate(self.alarmanlage, partition)  
            elif command == 'check':
                result = self.check_ob_zu(partition)    
                broadcast_input_value('Secvest.Check.Done', str(1))
            #alarmanlage.logout()
            self.commandActive = False
            return result
        except Exception as e:
            print(e)
#            aes.new_event(description="Secvest konnte nicht bedient werden", prio=9)
            payload = {'Szene':'SecvestInfo', 'desc':'Secvest konnte nicht bedient werden'}
            toolbox.communication.send_message(payload, typ='ExecSzene')            
            self.commandActive = False
            return False
               
    def receive_communication(self, payload, *args, **kwargs):
        if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'Secvest':
            adress=toolbox.kw_unpack(kwargs,'adress')
            partition = int(adress.split(".")[1])
            new_pl = {}
            new_pl['Value'] = True
            #new_pl['SleepTime'] = payload['SleepTime']
            result = self.set_device(payload['command'], partition)          
            toolbox.communication.send_message(payload, typ='return', value=result)            
          
    def pause_monitoring(self):
        if constants.run and bool(eval(str(msqc.setting_r("PauseSecvest")))):
            if self.alarmanlage:
                print('secvest logging out')
                self.alarmanlage.logout()
            counter = 0
            while bool(eval(str(msqc.setting_r("PauseSecvest")))):
                time.sleep(1)    
                counter += 1
                if counter > 3600:
                    msqc.setting_s("PauseSecvest", False)
            if constants.run:
                self.alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
            
    def monitor(self):
        logged = True
        while constants.run and logged:
            self.pause_monitoring()
            while constants.run and self.commandActive:
                time.sleep(1)
            self.pause_monitoring()
            self.checkActive = True
            try:
                self.check_ob_zu()
                self.get_alarms()
                self.get_faults()                
            except:
                try:
                    print('einloggen secvest')
                    self.alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
                    print('Eingeloggt secvest')
                    self.check_ob_zu()
                except:
                    print('Secvest einloggen fehlgeschlagen')
                    logged = False
            self.checkActive = False
            self.pause_monitoring()
            toolbox.sleep(self.cycleTime)
        if self.alarmanlage is not None:
            print('Secvest lgging out')
            self.alarmanlage.logout()
        print('Secvest logged out')
            
            
            


def main():
    try:     
        sv = SecvestHandler()            
        reg_id = toolbox.communication.register_callback(sv.receive_communication) 
        sv.monitor()   
    except Exception as e:
        print(e)    
    toolbox.communication.unregister_callback(reg_id)         

if __name__ == "__main__":
    main()
