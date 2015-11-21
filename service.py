#!  /usr/bin/python

import threading
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time, os
import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://192.168.192.1',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

led = LEDs()
t = threading.Thread(target=led.start, args = [0.25])
t.start()

keys = usb_key()
t = threading.Thread(target=keys.monitor, args = [])
t.start()

tuer = tuer_switch()
t = threading.Thread(target=tuer.monitor, args = [])
t.start()

led.schalte(led.aus,led.f1,led.aus)


while not internet_on():
    time.sleep(10)
    #os.system('sudo killall python')

PORT_NUMBER = 5000
hostName = gethostbyname( '192.168.192.32' )
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )
SIZE = 1024

led.schalte(led.aus,led.aus,led.aus)

os.system('sudo mount -a')

while True:
    (data,addr) = mySocket.recvfrom(SIZE)
    isdict = False
    try:
        data_ev = eval(data)
        if type(data_ev) is dict:
            if "erinnern" in str(data):
                led.schalte(data_ev.get("Rot"),data_ev.get("Gelb"),data_ev.get("Gruen"),data_ev.get("erinnern"))
            else:
                led.schalte(data_ev.get("Rot"),data_ev.get("Gelb"),data_ev.get("Gruen"))
            isdict = True
    except Exception as serr:
        lgd.debug(" NameError " + str(serr))
        isdict = False                