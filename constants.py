#!  /usr/bin/python 

import ConfigParser

config = ConfigParser.RawConfigParser()

cfg_main={'eigene_IP':'192.168.192.10', 'name':'BueroPi',\
        'xs1_IP':'192.168.192.4','router_IP':'192.168.192.1','UDP_PORT':'5000',\
        'installation_folder':'/home/pi/steuerzentrale','temp_folder':'/home/pi/temp/',\
        'gcm_ID':'', 'automatic_backup':'False', 'webcam_supervision':'False',\
        'tts':'False','heartbt':'125'}
cfg_xs1 ={'USER':'admin','PASS':'admin'}

def init_cfg():
    if not config.has_section('Main'):
        config.add_section('Main')
    for cfg in cfg_main:
        if not config.has_option('Main', cfg):
            config.set('Main', cfg, cfg_main.get(cfg))
    if not config.has_section('XS1'):
        config.add_section('XS1')
    for cfg in cfg_xs1:
        if not config.has_option('XS1', cfg):
            config.set('XS1', cfg, cfg_xs1.get(cfg))            
    
    # Writing our configuration file to 'main.cfg'
    with open('main.cfg', 'wb') as configfile:
        config.write(configfile)



for i in range(0,3):
    while True:
        try:
            run = True
            config.readfp(open('main.cfg'))
            eigene_IP = config.get('Main', 'eigene_IP')
            name = config.get('Main', 'name')
            
            xs1_IP = config.get('Main', 'xs1_IP')
            router_IP = config.get('Main', 'router_IP')
            UDP_PORT = config.getint('Main', 'UDP_PORT')
            installation_folder = config.get('Main', 'installation_folder')
            temp_folder = config.get('Main', 'temp_folder')
            gcm_ID = config.get('Main', 'gcm_ID')
            
            automatic_backup = config.getboolean('Main', 'automatic_backup')
            webcam_supervision = config.getboolean('Main', 'webcam_supervision')
            tts = config.getboolean('Main', 'tts')
        
            #timeout for connection in seconds
            heartbt = config.getint('Main', 'heartbt')
            
            class xs1_:
                STREAM_URL = xs1_IP+"/control?callback=cname&cmd=subscribe&format=txt" 
                # constants.xs1_.IP    
                IP = xs1_IP
                USER = config.get('XS1', 'USER')
                PASS = config.get('XS1', 'PASS')            
        except:
            init_cfg()
            continue
        break


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
    #move to mysql_com
    #historic logs
    his_inputs      = sql_object("HIS_inputs", "Historic", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"), ("Name","VARCHAR(20)"), ("Value","DECIMAL(5,1)"), ("Date","DATETIME")))
    #alarm_events    = sql_object("HIS_alarmevents", "Historic", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"), ("Description","VARCHAR(20)"),("Prio","DECIMAL(2,0)"),("Date","DATETIME"),("Acknowledged","DATETIME")))
    #command tables
    inputs          = sql_object("cmd_inputs", "Commands", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Input","VARCHAR(20)"),("Logging","tinyint(1)"),("Setting","tinyint(1)"),("last1","DATETIME"),("last2","DATETIME"), ("Value_lt","DECIMAL(5,2)"),("Value_eq","DECIMAL(5,2)"),("Value_gt","DECIMAL(5,2)"),( "Wach","VARCHAR(20)"), ("Schlafen","VARCHAR(20)"), ("Schlummern","VARCHAR(20)"),("Leise","VARCHAR(20)"), ("AmGehen","VARCHAR(20)"), ("Gegangen","VARCHAR(20)"), ("Abwesend","VARCHAR(20)"), ("Urlaub","VARCHAR(20)"), ("Besuch","VARCHAR(20)"), ("Doppel","VARCHAR(20)"), ("Dreifach","VARCHAR(20)")))
    settings        = sql_object("set_settings", "Settings", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("Value","VARCHAR(45)"),("inApp","VARCHAR(45)"),("Beschreibung","VARCHAR(45)")))
    
    #move to cron
    cron            = sql_object("cmd_cron", "Commands", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Szene","VARCHAR(45)"),("Time","TIME"),("Bedingung","varchar(45)"),("Permanent","tinyint(4)"),("Mo","tinyint(1)"),("Tu","tinyint(1)"),("Wed","tinyint(1)"),("Th","tinyint(1)"),("Fr","tinyint(1)"),("Sa","tinyint(1)"),("Su","tinyint(1)"),("Enabled","tinyint(4)"),("Sonne","varchar(45)"),("offset","varchar(45)"),("Zufall","varchar(45)"),("Rohtime","TIME")))
    wecker          = sql_object("cmd_wecker", "Commands", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("Enabled","tinyint(1)"),("Mo","tinyint(1)"),("Tu","tinyint(1)"),("Wed","tinyint(1)"),("Th","tinyint(1)"),("Fr","tinyint(1)"),("Sa","tinyint(1)"),("Su","tinyint(1)"),("offset","varchar(45)"),("Szene","VARCHAR(45)"),("Time","TIME"),("Bedingung","varchar(45)"),("Permanent","tinyint(4)")))
    ##tables with settings
    #hue_autolight   = sql_object("set_hue_autolicht", "Settings", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("offset","INT(11)"),("min","INT(11)"),("max","INT(11)")))
    
    #move to szenen
    szenen          = sql_object("set_Szenen", "Settings", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("Prio","INT(11)"),("Beschreibung","TEXT"),("Durchsage","TEXT"),("Gruppe","VARCHAR(45)"),("inApp","VARCHAR(45)"),("Setting","TEXT"),("Follows","TEXT"),("Bedingung","TEXT"),("AutoMode","VARCHAR(45)"),("setTask","VARCHAR(45)"),("setTaskZuhause","VARCHAR(45)"),("intCmd","VARCHAR(45)"),("LastUsed","DATETIME")))
    
    #move to sats
    #satellites      = sql_object("set_satellites", "Settings", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("IP","VARCHAR(45)"),("PORT","INT(11)"),("Type","VARCHAR(45)"),("USER","VARCHAR(45)"),("PASS","VARCHAR(45)"),("command_set","VARCHAR(45)")))
    
    ##tables for outputs
    #hue             = sql_object("out_hue", "Outputs", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("hue","VARCHAR(45)"),("bri","VARCHAR(45)"),("sat","VARCHAR(45)"),("an","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))
    LightstripSchlafzi = sql_object("out_LightstripSchlafzi", "Outputs", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("rot","VARCHAR(45)"),("gruen","VARCHAR(45)"),("blau","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))
    Marantz         = sql_object("out_Marantz", "Outputs",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("PWR","VARCHAR(45)"),("VOL","VARCHAR(45)"),("SRC","VARCHAR(45)"),("AMT","VARCHAR(45)"),("DIP","VARCHAR(45)")))
    Sideboard       = sql_object("out_Sideboard", "Outputs",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("rot","VARCHAR(45)"),("gruen","VARCHAR(45)"),("blau","VARCHAR(45)"),("transitiontime","VARCHAR(45)")))
    #Sonos           = sql_object("out_Sonos", "Outputs",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("MasterZone","VARCHAR(45)"),("Pause","INT(4)"),("Sender","VARCHAR(300)"),("Radio","INT(4)"),("TitelNr","VARCHAR(45)"),("Time","TIME"),("PlaylistNr","VARCHAR(45)"),("Volume","VARCHAR(45)")))
    TuerSPi         = sql_object("out_TuerSPi", "Outputs",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("rot","VARCHAR(20)"),("gruen","VARCHAR(20)"),("gelb","VARCHAR(20)")))
    ##setting tables with sensible data
    Besucher        = sql_object("sst_Besucher", "SensData",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("Handy_IP","VARCHAR(20)"),("Handy_State","INT(11)"),("USB_ID","VARCHAR(45)"),("USB_State","INT(4)"),("prod","VARCHAR(45)"),("gcm_regid","VARCHAR(255)"),("gcm_name","VARCHAR(50)")))
    Bewohner        = sql_object("sst_Bewohner", "SensData",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("Handy_IP","VARCHAR(20)"),("Handy_State","INT(11)"),("USB_ID","VARCHAR(45)"),("USB_State","INT(4)"),("prod","VARCHAR(45)"),("gcm_regid","VARCHAR(255)"),("gcm_name","VARCHAR(50)"))) 
    
    
    tables = [his_inputs,inputs,cron,wecker,settings,szenen,LightstripSchlafzi,Marantz,Sideboard,TuerSPi,Besucher,Bewohner]
    HUE = sql_object("HUE", "HUE",('BettChris', 'Stablampe_1', 'Stablampe_2', 'Lightstrip_Eingang', 'Lightstrip_Kueche', 'Balkonlampe', 'Stehlampe', 'BettSabina', 'Buero', 'Bad', 'Monaco_Lampe'))
    SATELLITE = sql_object("SATELLITE", "SATELLITE",('Sideb_links', 'LightstripSchlafzi', 'Sideb_mitte', 'Sideb_rechts', 'Marantz', 'Sideb_oben', 'TuerSPi','Scanner'))
    XS1 = sql_object("XS1", "XS1",('Sideboard', 'Kueche', 'Diele', 'Video_Audio', 'Lattenrost', 'Wohnzimmer_Decke', 'Schlafzimmer', 'Webcams', 'Elchlampe', 'Adventslichter', 'Reduit', 'Pflanzen', 'Saugstauber', 'PC_Peripherie', 'Weihnachtsbaum', 'Esszimmer','Rauchmelder'))
    SONOS = sql_object("SONOS", "SONOS",('SonosWohnZi','SonosKueche','SonosBad','SonosSchlafZi'))
    TV  = sql_object("TV", "TV",('TV',))
    inps = (TV, SONOS, SATELLITE, HUE, XS1)
    
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