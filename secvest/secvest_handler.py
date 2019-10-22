# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:36:06 2019

@author: hc
"""

import constants
import toolbox
from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()


from secvest.secvest import Secvest

def broadcast_input_value(Name, Value):
    payload = {'Name':Name,'Value':Value}
#    on server:
    toolbox.log(Name, Value, level=9)
    toolbox.communication.send_message(payload, typ='InputValue')

def activate(partition=1):
    alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
    alarmanlage.set_partition(partition)
#    check
    success = False
    status_part = alarmanlage.get_partition(partition)
    if status_part['stats'] == 'set':
        print('ok')
        aes.new_event(description="Secvest aktiv", prio=9)
        broadcast_input_value('Secvest.Partition' + str(partition), str(1))
        success = True
    else:
        aes.new_event(description="Secvest konnte nicht aktiviert werden", prio=9)
        print('Konnte die Partition nicht aktivieren')
    alarmanlage.logout()
    return success
    
def deactivate(partition=1):
    alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password)
    alarmanlage.unset_partition(partition)
#    check
    success = False
    status_part = alarmanlage.get_partition(partition)
    if status_part['stats'] == 'unset':
        print('ok')
        aes.new_event(description="Secvest deaktiviert", prio=9)
        broadcast_input_value('Secvest.Partition' + str(partition), str(0))
        success = True
    else:
        print('Konnte die Partition nicht deaktivieren')
        aes.new_event(description="Secvest konnte nicht deaktiviert werden", prio=9)
    alarmanlage.logout()
    return success    
    
def __check_zones__(alarmanlage, partition=1, liste=None):
    if liste is None:
        liste = []
    zonen = alarmanlage.get_zones_by_partition(partition)
    for zone in zonen:
        if zone['state'] != 'closed':
            broadcast_input_value('Secvest.Partition' + str(partition) + '.' + zone['name'], str(1))
        else:
            broadcast_input_value('Secvest.Partition' + str(partition) + '.' + zone['name'], str(0))            
        liste.append(zone)
    
def check_ob_zu(partition=None):
    liste = []
    alarmanlage = Secvest(hostname=constants.secvest.hostname, username=constants.secvest.username, password=constants.secvest.password) 
    if partition is None:
        for partition in range(1,5):
            __check_zones__(alarmanlage, partition, liste)
    else:
        __check_zones__(alarmanlage, partition, liste)        
    alarmanlage.logout() 
    result = True
    for zone in liste:
        if zone['state'] != 'closed':
            aes.new_event(description=zone['name'] + ' ist nicht geschlossen', prio=9)
            print(zone['name'], ' ist nicht geschlossen')
            result = False
    return result

           
def receive_communication(payload, *args, **kwargs):
    if toolbox.kw_unpack(kwargs,'typ') == 'output' and toolbox.kw_unpack(kwargs,'receiver') == 'Secvest':
        adress=toolbox.kw_unpack(kwargs,'adress')
        partition = int(adress.split(".")[1])
        new_pl = {}
        new_pl['Value'] = payload['Value']
        new_pl['SleepTime'] = payload['SleepTime']
        result = False
        if payload['command'] == 'activate':
            result = activate(partition)
        elif payload['command'] == 'deactivate':
            result = deactivate(partition)  
        elif payload['command'] == 'check':
            result = check_ob_zu(partition)             
        toolbox.communication.send_message(payload, typ='return', value=result)            
            
toolbox.communication.register_callback(receive_communication)            