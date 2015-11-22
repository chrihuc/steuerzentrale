sudo apt-get install daemontools
sudo apt-get install daemontools-run

sudo mkdir /etc/service

sudo mkdir /etc/service/daemon

sudo nano /etc/service/daemon/run

#!/bin/sh
exec 2>&1
exec setuidgid root sh -c '
  exec /usr/bin/python /home/chris/homecontrol/xs1inputs.py
'

sudo chmod 755 /etc/service/daemon/run



mkdir /etc/service/daemon/log

sudo nano /etc/service/daemon/log/run

#!/bin/sh
     exec setuidgid root multilog t /home/chris/homecontrol/logxs1inp

sudo chmod 755 /etc/service/daemon/log/run



#####################################3
sudo apt-get install python-dev 

sudo apt-get install python-mysqldb
sudo nano /etc/mysql/my.cnf
#bind-address 127.0.0.1
sudo service mysql restart
sudo apt-get install python-pip
sudo pip install phue
sudo pip install gcm
sudo apt-get install python-pycurl
sudo apt-get install python-pysolar


python

from phue import Bridge
b = Bridge('192.168.192.190')

