sudo apt-get install daemontools
sudo apt-get install daemontools-run

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



#####################################3
sudo apt-get install python-dev         #??

sudo apt-get install python-mysqldb     #??

sudo nano /etc/mysql/my.cnf
#bind-address 127.0.0.1

sudo service mysql restart

sudo apt-get install python-pip         #??
sudo pip install phue                   #??
sudo pip install gcm                    #??
sudo apt-get install python-pycurl      #??
sudo apt-get install python-pysolar     #??
sudo pip install pyephem                #??
sudo pip install paramiko               #??
sudo apt-get install python-dateutil    #python3

python

from phue import Bridge
b = Bridge('192.168.192.190')

