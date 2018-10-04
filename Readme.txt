This repo is thought mainly for my own use, it's
 - not yet cleaned up
 - the installer is not ready
 - parts of it were written 10 years ago
 -> you can see my python skills developing over the years
 - I did not care to follow pep8 rules strictly
 - instead of unittests I wrote the modules to be standalone
Feel free to roam and explore and use whatever you like.

###################################
needed packages
###################################

git clone https://github.com/chrihuc/steuerzentrale.git sz
cd sz


sudo apt-get install daemontools daemontools-run python-dev python-mysqldb python-pip python-pycurl python-pysolar python-dateutil python-pymad python-pip python-paramiko espeak python-pandas
sudo pip install phue gcm pyephem paramiko tinkerforge gitpython pyqtgraph easygui soco paho-mqtt

python-pyaudio (xprintidle feh) python3-pyaudio

sudo pip install phue                   #??
sudo pip install gcm                    #??
sudo pip install pyephem                #??
sudo pip install paramiko               #??
sudo pip install tinkerforge
sudo pip install gitpython
sudo pip install pyqtgraph
sudo pip install easygui
sudo pip install gitpython
sudo pip install kivy
sudo apt-get install python-kivy

sudo pip install kivy-garden
sudo garden install graph


python constants.py
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

###################################
needed packages python3
###################################

python3-pandas
python3-paho-mq
python3-mysqldb
python3-ephem
python3-urllib3
python3-git
python3-paramiko
python3-pycurl
pip3 phue 

pyqtgraph easygui

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
