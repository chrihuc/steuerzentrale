#!  /usr/bin/python 

eigene_IP = "192.168.192.33"
xs1_IP = "192.168.192.4"
router_IP = "192.168.192.1"
UDP_PORT = 5000
installation_folder = "/home/pi/steuerzentrale"
gcm_ID = 'AIzaSyCF_dmQYm9qjfry3sG_RDGYxYQMMgFMbts'

#timeout for connection in seconds
heartbt = 125

class xs1_:
    STREAM_URL = xs1_IP+"/control?callback=cname&cmd=subscribe&format=txt" 
    # constants.xs1_.IP    
    IP = xs1_IP
    USER = "admin"
    PASS = "admin"
    
class sql_:
    # constants.sql_.IP
    IP = eigene_IP
    USER = "customer"
    PASS = "user"
    DB = "XS1DB"
    
class udp_:
    IP = eigene_IP
    # constants.udp_.PORT
    PORT = UDP_PORT
    
class scanner_:
    # constants.scanner_.IP
    IP = "192.168.192.10"
    # constants.scanner_.PORT
    PORT = 5010
    
class hue_:
    # hue lights for notification
    # constants.hue_.devices
    notify_devices = ['Stehlampe','Stablampe 1', 'Stablampe 2', 'LightStrips 2']
    # constants.hue_.IP
    IP = "192.168.192.190"    
    
class mail_:
    # constants.mail_.receiver
    receiver = "chrihuc@gmail.com"
    