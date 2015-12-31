###################################
needed packages
###################################
sudo apt-get install daemontools daemontools-run python-dev python-mysqldb python-pip python-pycurl python-pysolar python-dateutil python-pymad python-pip

sudo pip install phue                   #??
sudo pip install gcm                    #??
sudo pip install pyephem                #??
sudo pip install paramiko               #??
sudo pip install tinkerforge

##################################
setup of daemon tools
##################################
sudo mkdir /etc/service
sudo mkdir /etc/service/steuerzentrale
sudo nano /etc/service/steuerzentrale/run

#!/bin/sh
exec 2>&1
exec setuidgid root sh -c '
  exec /usr/bin/python /home/pi/steuerzentrale/main.py
'

sudo chmod 755 /etc/service/steuerzentrale/run

sudo mkdir /etc/service/steuerzentrale/log
sudo nano /etc/service/steuerzentrale/log/run

#!/bin/sh
     exec setuidgid root multilog t /home/pi/steuerzentrale/log

sudo chmod 755 /etc/service/steuerzentrale/log/run

#####################################
open mysql to intranet
#####################################
sudo nano /etc/mysql/my.cnf
#bind-address 127.0.0.1
sudo service mysql restart

####################################
open hue pod
####################################
python / sudo python

from phue import Bridge
b = Bridge('192.168.192.190')


########################
howto add a Satellite virtuel or real
########################
device Satellite in Szenen
Table with the Satellites name and commands to send
Satellite with IP and Port in table Satellites

###########
todo:
    
    gcm setting id is empty

V1: separate szenen
        Interlocks für PS3 o.ä?
        write back correct status of aktuatoren
    add "empty" sattelite for all TiFo aktuatoren
    finish doppelklick und dreifachklick
        bei dreifachklick wird doppelklick und einfach auch ausgeführt
    move table creation to cmd_modules
    rewrite communication to acknowledge
    szenen_timer is recursive not working
    satellites add thread supervision
    scanner is satellite
    historic tables in reverse
    forced restart start also all satellites
    add logging into receiving
    Use new Key as input events
    alarm event missing hue feedback