#!  /usr/bin/python

import constants

import threading
#from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os, sys
#import urllib2
import xs1inputs, udpinputs, redundancy, periodic_sup

threadliste = []

t = threading.Thread(target=xs1inputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=udpinputs.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=redundancy.main, args = [])
threadliste.append(t)
t.start()

t = threading.Thread(target=periodic_sup.main, args = [])
threadliste.append(t)
t.start()

#print threadliste
#add supervision of threads

try:
    while constants.run:
        for t in threadliste:
            if not t in threading.enumerate():
                constants.run = False
                sys.exit() 
        time.sleep(1)
except KeyboardInterrupt:
    constants.run = False
    sys.exit() 
 
    
