###################################
needed packages
###################################

git clone https://github.com/chrihuc/steuerzentrale.git sz
cd sz

sudo apt-get install daemontools daemontools-run python-dev python-mysqldb python-pip 
python-pycurl python-pysolar python-dateutil python-pymad python-pip python-pyaudio 
python3-pyaudio espeak python-pandas xprintidle feh
sudo pip install phue gcm pyephem paramiko tinkerforge gitpython pyqtgraph easygui soco

sudo pip install phue                   #??
sudo pip install gcm                    #??
sudo pip install pyephem                #??
sudo pip install paramiko               #??
sudo pip install tinkerforge
sudo pip install gitpython
sudo pip install pyqtgraph
sudo pip install easygui
sudo pip install gitpython

##################################
setup of daemon tools
##################################
sudo mkdir /etc/service
sudo mkdir /etc/service/steuerzentrale
sudo nano /etc/service/steuerzentrale/run

#!/bin/sh
exec 2>&1
cd /home/pi/steuerzentrale/
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
    change names
        sonos in module
        xs1 on device
        hue on device
        sats on mysql
    neue Szene tut nicht
    dupliziere Input
    neuer Befehl
    gebe wert bis zu endgütlig command weiter
    check if hue command was executed only then return true
    gcm setting id is empty
    szenen gui
    input gui

issue:
    szenen commands coming back as string

V1: separate szenen
        Interlocks für PS3 o.ä?
        write back correct status of aktuatoren
    tv on with sattelite
    add "empty" sattelite for all TiFo aktuatoren
    finish doppelklick und dreifachklick
        bei dreifachklick wird doppelklick und einfach auch ausgeführt
    satellites add thread supervision
    scanner is satellite
    historic tables in reverse
    forced restart start also all satellites
    Use new Key as input events
    ensure wecker is really working
