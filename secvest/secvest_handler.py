# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:36:06 2019

@author: hc
"""

import time

import constants
from tools import toolbox
from alarm_event_messaging import alarmevents as aevs
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


    def activate(self, alarmanlage, partition=1):
        alarmanlage.set_partition(partition)
    #    check
        success = False
        status_part = alarmanlage.get_partition(partition)
        if status_part['state'] == 'set':
            print('ok')
            aes.new_event(description="Secvest aktiv", prio=9)
            broadcast_input_value('Secvest.Partition' + str(partition), str(1))
            success = True
        else:
            aes.new_event(description="Secvest konnte nicht aktiviert werden", prio=9)
            self.__check_zones__(partition, hinweis=True)
            print('Konnte die Partition nicht aktivieren')
        return success
    
    def deactivate(self, alarmanlage, partition=1):
        alarmanlage.unset_partition(partition)
    #    check
        success = False
        status_part = alarmanlage.get_partition(partition)
        if status_part['state'] == 'unset':
            print('ok')
            aes.new_event(description="Secvest deaktiviert", prio=9)
            broadcast_input_value('Secvest.Partition' + str(partition), str(0))
            success = True
        else:
            print('Konnte die Partition nicht deaktivieren')
            aes.new_event(description="Secvest konnte nicht deaktiviert werden", prio=9)
        return success    
        
    def __check_zones__(self, partition=1, hinweis=False):
        zonen = self.alarmanlage.get_zones_by_partition(partition)
        for zone in zonen:
            if zone['state'] != 'closed':
                broadcast_input_value('Secvest.Partition' + str(partition) + '.' + zone['name'], str(1))
                if hinweis:
                    aes.new_event(description=zone['name'] + ' ist nicht geschlossen', prio=9)
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
            aes.new_event(description="Secvest konnte nicht bedient werden", prio=9)
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
            
    def monitor(self):
        while True:
            while self.commandActive:
                time.sleep(1)
            self.checkActive = True
            try:
                self.check_ob_zu()
            except:
                self.alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
                self.check_ob_zu()
            self.checkActive = False
            time.sleep(self.cycleTime)            
            
            
            


def main():
    sv = SecvestHandler()            
    toolbox.communication.register_callback(sv.receive_communication)            
    sv.monitor()             

if __name__ == "__main__":
    main()
