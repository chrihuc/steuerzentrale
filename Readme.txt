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
    wecker from cron not wecker.py
    remove temperatur prediction

V1: rewrite communication to acknowledge
    szenen_timer is recursive not working
    Einer wach wird Nachtruhe
    Alle inputs in einen Table
    Tables ordern historische vs Einstellungen d sensible Daten
    setup creates all tables in sql root password not stored