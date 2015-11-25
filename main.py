#!  /usr/bin/python

import threading
#from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os
#import urllib2
import xs1inputs, udpinputs, redundancy

#periodic_sup

t = threading.Thread(target=xs1inputs.main, args = [])
t.start()

t = threading.Thread(target=udpinputs.main, args = [])
t.start()

t = threading.Thread(target=redundancy.main, args = [])
t.start()

while True:
    time.sleep(1)