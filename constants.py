#!  /usr/bin/python 

from collections import OrderedDict

run = True

eigene_IP = "192.168.192.33"
name = "BueroPi"

xs1_IP = "192.168.192.4"
router_IP = "192.168.192.1"
UDP_PORT = 5000
installation_folder = "/home/pi/steuerzentrale"
temp_folder = "/home/pi/temp/"
gcm_ID = ''

automatic_backup = False
webcam_supervision = False
tts = False

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
    DB = "Steuerzentrale"

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns    
    
class sql_tables:
    #historic logs
    his_inputs      = sql_object("HIS_inputs", "Historic", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"), ("Name","VARCHAR(20)"), ("Value","DECIMAL(5,1)"), ("Date","DATETIME")))
    alarm_events    = sql_object("HIS_alarmevents", "Historic", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"), ("Description","VARCHAR(20)"),("Prio","DECIMAL(2,0)"),("Date","DATETIME"),("Acknowledged","DATETIME")))
    #command tables
    inputs          = sql_object("cmd_inputs", "Commands", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Inputs","VARCHAR(20)"), ("Value_lt","DECIMAL(5,2)"),("Value_eq","DECIMAL(5,2)"),("Value_gt","DECIMAL(5,2)"),( "Wach","VARCHAR(20)"), ("Schlafen","VARCHAR(20)"), ("Ruhezeit","VARCHAR(20)"), ("AmGehen","VARCHAR(20)"), ("Gegangen","VARCHAR(20)"), ("Abwesend","VARCHAR(20)"), ("Urlaub","VARCHAR(20)"), ("Besuch","VARCHAR(20)")))
    cron            = sql_object("cmd_cron", "Commands", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Szene","VARCHAR(45)"),("Time","time"),("Bedingung","varchar(45)"),("Permanent","tinyint(4)"),("Mo","tinyint(1)"),("Tu","tinyint(1)"),("Wed","tinyint(1)"),("Th","tinyint(1)"),("Fr","tinyint(1)"),("Sa","tinyint(1)"),("Su","tinyint(1)"),("Enabled","tinyint(4)"),("Sonne","varchar(45)"),("offset","varchar(45)"),("Zufall","varchar(45)"),("Rohtime","time")))
    #wecker          = sql_object("cmd_wecker"
    #usb_key_actions = sql_object("cmd_KeyActions"
    #hue_autolight   = sql_object("cmd_hue_autolicht"
    ##tables with settings
    #settings        = sql_object("set_settings"
    #szenen          = sql_object("set_Szenen"
    #satellites      = sql_object("set_satellites"
    ##tables for outputs
    #hue             = sql_object("out_hue"
    #LightstripSchlafzi = sql_object("out_LightstripSchlafzi"
    #Marantz         = sql_object("out_Marantz"
    #Sideboard       = sql_object("out_Sideboard"
    #Sonos           = sql_object("out_Sonos"
    #TuerSPi         = sql_object("out_TuerSPi"
    ##setting tables with sensible data
    #Besucher        = sql_object("sst_Besucher"
    #Bewohner        = sql_object("sst_Bewohner"
    #gcm_user        = sql_object("sst_gcm_users"   
    tables = [his_inputs,alarm_events,inputs,cron]
    
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
    receiver = ""
    
class redundancy_:
    # constants.redundancy_.master
    master = False   
    timeout_receive = 10
    timeout_send = 1
    partner_IP = "192.168.192.10"
    PORT = 5050    
    #'Master' 'Slave' 'auto'
    typ = 'Slave'