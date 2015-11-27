#!/usr/bin/env python

import constants

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Timer
import time
from alarmevents import alarm_event

hostName = gethostbyname( constants.eigene_IP )
SIZE = 1024

aes = alarm_event()

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, constants.redundancy_.PORT) )

def set_master():
    constants.redundancy_.master = True
    time.sleep(1)
    aes.new_event(description="Master-Slave changeover, " + constants.name + " ist Master", prio=5, durchsage="", karenz=0)
    while constants.run:
        mySocket.sendto("master",(constants.redundancy_.partner_IP,constants.redundancy_.PORT))
        time.sleep(constants.redundancy_.timeout_send)
        
def set_master_fake():
    aes.new_event(description="Fake Master-Slave changeover, " + constants.name + " ist Master", prio=5, durchsage="", karenz=0)     

def main():
    if constants.redundancy_.typ == 'Master':
        set_master()
    elif constants.redundancy_.typ == 'Slave':
        aes.new_event(description="Running as slave", prio=0, durchsage="", karenz=0)
        constants.redundancy_.master = False
        redundancy = Timer(constants.redundancy_.timeout_receive, set_master_fake)
        redundancy.start() 
        while constants.run:
                (data,addr) = mySocket.recvfrom(SIZE)            
                if (data == "master"):         
                    redundancy.cancel()
                    redundancy = Timer(constants.redundancy_.timeout_receive, set_master_fake)
                    redundancy.start()       
    elif constants.redundancy_.typ == 'auto':
        redundancy = Timer(constants.redundancy_.timeout_receive, set_master)
        redundancy.start() 
        aes.new_event(description="Master-Slave redundancy started", prio=0, durchsage="", karenz=0)
        while constants.run:
                (data,addr) = mySocket.recvfrom(SIZE)            
                if (data == "master"):         
                    redundancy.cancel()
                    redundancy = Timer(constants.redundancy_.timeout_receive, set_master)
                    redundancy.start()       
    
    
if __name__ == '__main__':
    main()    
