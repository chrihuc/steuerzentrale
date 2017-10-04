#!  /usr/bin/python
 
import constants 
 
import socket
import base64
import time
import re
import sys, os
from socket import error as socket_error

from database import mysql_connector

# TODO Tests split adress from hks

def ping(IP, number = 1):
    pinged = False
    if IP == None:
        return False
    else:
        lifeline = re.compile(r"(\d) received")
        report = ("No response","Partial Response","Alive")         
        for i in range(0,number):
            pingaling = os.popen("ping -q -c 2 "+IP,"r")
            sys.stdout.flush()
            while 1==1:
               line = pingaling.readline()
               if not line: break
               igot = re.findall(lifeline,line)
               if igot:
                if int(igot[0])==2:
                    pinged = True
                else:
                    pass
        return pinged


class Remotecontrol:
    def __init__(self,myip,tvip,mymac):
        self.data = []
        self.my_ip = str(myip)
        self.tv_ip = str(tvip)
        self.my_mac = str(mymac)        
        #What the iPhone app reports
        self.appstring = "iphone..iapp.samsung"
        #Might need changing to match your TV type
        self.tvappstring = "iphone.UE55C8000.iapp.samsung"
        #What gets reported when it asks for permission
        self.remotename = "Python Samsung Remote"
    
    def authenti(self):
        # First configure the connection  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.tv_ip, 55000))
        ipencoded = base64.b64encode(self.my_ip)
        macencoded = base64.b64encode(self.my_mac)
        messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
        + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
        + macencoded + chr(len(base64.b64encode(self.remotename))) + chr(0x00) \
        + base64.b64encode(self.remotename)
     
        part1 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
        + chr(len(messagepart1)) + chr(0x00) + messagepart1
        sock.send(part1)
         
        messagepart2 = chr(0xc8) + chr(0x00)
        part2 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
        + chr(len(messagepart2)) + chr(0x00) + messagepart2
        sock.send(part2)    

    def send_core(self,sock,key):
        messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
        part3 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
        sock.send(part3)
        time.sleep(0.3)        
        
    # Function to send keys
    def sendKey(self, skey):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        for i in range(0,90):
            if ping(self.tv_ip):
                break
            else:
                time.sleep(1.0)     
        try:
            sock.connect((self.tv_ip, 55000))
            # First configure the connection 
            if (1==1):
                ipencoded = base64.b64encode(self.my_ip)
                macencoded = base64.b64encode(self.my_mac)
                messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
                + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
                + macencoded + chr(len(base64.b64encode(self.remotename))) + chr(0x00) \
                + base64.b64encode(self.remotename)
                    
                part1 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
                + chr(len(messagepart1)) + chr(0x00) + messagepart1
                sock.send(part1)
                
                messagepart2 = chr(0xc8) + chr(0x00)
                part2 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
                + chr(len(messagepart2)) + chr(0x00) + messagepart2
                sock.send(part2)      
            for key in skey:
                #print key
                if key == 'max_vol':
                    for i in range(0,100):
                        self.send_core(sock, "KEY_VOLUP")
                    for i in range(0,10):
                        self.send_core(sock, "KEY_VOLDOWN")                        
                else:
                    self.send_core(sock, key)
            sock.close()
            return True
        except socket_error as serr:
            return False   

class TV:
    def __init__(self):
        #self.tv_remote = remotecontrol('192.168.192.10','192.168.192.26','00:30:1b:a0:2f:05')
        own_ip = constants.eigene_IP
        self.tv_remote_lan = Remotecontrol(own_ip,'192.168.192.29','00:30:1b:a0:2f:05')         
        
    def set_device(self,device, commd):       
        if self.tv_remote_lan.sendKey([str(commd)]): # or self.tv_remote.sendKey([str(commd)]):
            return True
        else:
            return False
     
    def list_commands(self):
        #comands = mdb_get_table(table.name)
        liste = []
    # Normal remote keys
        liste += ["KEY_0"]
        liste += ["KEY_1"]
        liste += ["KEY_2"]
        liste += ["KEY_3"]
        liste += ["KEY_4"]
        liste += ["KEY_5"]
        liste += ["KEY_6"]
        liste += ["KEY_7"]
        liste += ["KEY_8"]
        liste += ["KEY_9"]
        liste += ["KEY_UP"]
        liste += ["KEY_DOWN"]
        liste += ["KEY_LEFT"]
        liste += ["KEY_RIGHT"]
        liste += ["KEY_MENU"]
        liste += ["KEY_PRECH"]
        liste += ["KEY_GUIDE"]
        liste += ["KEY_INFO"]
        liste += ["KEY_RETURN"]
        liste += ["KEY_CH_LIST"]
        liste += ["KEY_EXIT"]
        liste += ["KEY_ENTER"]
        liste += ["KEY_SOURCE"]
        liste += ["KEY_AD"] #KEY_PLAY
        liste += ["KEY_PAUSE"]
        liste += ["KEY_MUTE"]
        liste += ["KEY_PICTURE_SIZE"]
        liste += ["KEY_VOLUP"]
        liste += ["KEY_VOLDOWN"]
        liste += ["KEY_TOOLS"]
        liste += ["KEY_POWEROFF"]
        liste += ["KEY_CHUP"]
        liste += ["KEY_CHDOWN"]
        liste += ["KEY_CONTENTS"]
        liste += ["KEY_W_LINK"] #Media P
        liste += ["KEY_RSS"] #Internet
        liste += ["KEY_MTS"] #Dual
        liste += ["KEY_CAPTION"] #Subt
        liste += ["KEY_REWIND"]
        liste += ["KEY_FF"]
        liste += ["KEY_REC"]
        liste += ["KEY_STOP"]
        liste += ['max_vol']
    # Bonus buttons not on the normal remote:
        liste += ["KEY_TV"]
        return liste
     
    def dict_commands(self):
        #comands = mdb_get_table(table.name)
        dicti = {}
        itera = 1
        dicti[''] = itera
        liste = self.list_commands()
        for item in liste:
            itera +=1            
            dicti[str(item)] = itera
        return dicti  
     
    def list_devices(self):
        comands = mysql_connector.mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
        liste = []
        for comand in comands:
            if comands.get(comand) == "TV":
                liste.append(comand)
        #liste.remove("Name")
        return liste     
     
    #Don't work/wrong codes:
     #KEY_CONTENT
     #KEY_INTERNET
     #KEY_PC
     #KEY_HDMI1
     #KEY_OFF
     #KEY_POWER
     #KEY_STANDBY
     #KEY_DUAL
     #KEY_SUBT
     #KEY_CHANUP
     #KEY_CHAN_UP
     #KEY_PROGUP
     #KEY_PROG_UP


    
'''
KEY_0
KEY_1
KEY_2
KEY_3
KEY_4
KEY_5
KEY_6
KEY_7
KEY_8
KEY_9
KEY_11
KEY_12
KEY_3SPEED
KEY_4_3
KEY_16_9
KEY_AD
KEY_ADDDEL
KEY_ALT_MHP
KEY_ANGLE
KEY_ANTENA
KEY_ANYNET
KEY_ANYVIEW
KEY_APP_LIST
KEY_ASPECT
KEY_AUTO_ARC_ANTENNA_AIR
KEY_AUTO_ARC_ANTENNA_CABLE
KEY_AUTO_ARC_ANTENNA_SATELLITE
KEY_AUTO_ARC_ANYNET_AUTO_START
KEY_AUTO_ARC_ANYNET_MODE_OK
KEY_AUTO_ARC_AUTOCOLOR_FAIL
KEY_AUTO_ARC_AUTOCOLOR_SUCCESS
KEY_AUTO_ARC_CAPTION_ENG
KEY_AUTO_ARC_CAPTION_KOR
KEY_AUTO_ARC_CAPTION_OFF
KEY_AUTO_ARC_CAPTION_ON
KEY_AUTO_ARC_C_FORCE_AGING
KEY_AUTO_ARC_JACK_IDENT
KEY_AUTO_ARC_LNA_OFF
KEY_AUTO_ARC_LNA_ON
KEY_AUTO_ARC_PIP_CH_CHANGE
KEY_AUTO_ARC_PIP_DOUBLE
KEY_AUTO_ARC_PIP_LARGE
KEY_AUTO_ARC_PIP_LEFT_BOTTOM
KEY_AUTO_ARC_PIP_LEFT_TOP
KEY_AUTO_ARC_PIP_RIGHT_BOTTOM
KEY_AUTO_ARC_PIP_RIGHT_TOP
KEY_AUTO_ARC_PIP_SMALL
KEY_AUTO_ARC_PIP_SOURCE_CHANGE
KEY_AUTO_ARC_PIP_WIDE
KEY_AUTO_ARC_RESET
KEY_AUTO_ARC_USBJACK_INSPECT
KEY_AUTO_FORMAT
KEY_AUTO_PROGRAM
KEY_AV1
KEY_AV2
KEY_AV3
KEY_BACK_MHP
KEY_BOOKMARK
KEY_CALLER_ID
KEY_CAPTION
KEY_CATV_MODE
KEY_CHDOWN
KEY_CHUP
KEY_CH_LIST
KEY_CLEAR
KEY_CLOCK_DISPLAY
KEY_COMPONENT1
KEY_COMPONENT2
KEY_CONTENTS
KEY_CONVERGENCE
KEY_CONVERT_AUDIO_MAINSUB
KEY_CUSTOM
KEY_CYAN
KEY_BLUE(KEY_CYAN)
KEY_DEVICE_CONNECT
KEY_DISC_MENU
KEY_DMA
KEY_DNET
KEY_DNIe
KEY_DNSe
KEY_DOOR
KEY_DOWN
KEY_DSS_MODE
KEY_DTV
KEY_DTV_LINK
KEY_DTV_SIGNAL
KEY_DVD_MODE
KEY_DVI
KEY_DVR
KEY_DVR_MENU
KEY_DYNAMIC
KEY_ENTER
KEY_ENTERTAINMENT
KEY_ESAVING
KEY_EXIT
KEY_EXT1
KEY_EXT2
KEY_EXT3
KEY_EXT4
KEY_EXT5
KEY_EXT6
KEY_EXT7
KEY_EXT8
KEY_EXT9
KEY_EXT10
KEY_EXT11
KEY_EXT12
KEY_EXT13
KEY_EXT14
KEY_EXT15
KEY_EXT16
KEY_EXT17
KEY_EXT18
KEY_EXT19
KEY_EXT20
KEY_EXT21
KEY_EXT22
KEY_EXT23
KEY_EXT24
KEY_EXT25
KEY_EXT26
KEY_EXT27
KEY_EXT28
KEY_EXT29
KEY_EXT30
KEY_EXT31
KEY_EXT32
KEY_EXT33
KEY_EXT34
KEY_EXT35
KEY_EXT36
KEY_EXT37
KEY_EXT38
KEY_EXT39
KEY_EXT40
KEY_EXT41
KEY_FACTORY
        KEY_FAVCH
KEY_FF
KEY_FF_
KEY_FM_RADIO
KEY_GAME
KEY_GREEN
KEY_GUIDE
KEY_HDMI
KEY_HDMI1
KEY_HDMI2
KEY_HDMI3
KEY_HDMI4
KEY_HELP
KEY_HOME
KEY_ID_INPUT
KEY_ID_SETUP
KEY_INFO
KEY_INSTANT_REPLAY
KEY_LEFT
KEY_LINK
KEY_LIVE
KEY_MAGIC_BRIGHT
KEY_MAGIC_CHANNEL
KEY_MDC
KEY_MENU
KEY_MIC
KEY_MORE
KEY_MOVIE1
KEY_MS
KEY_MTS
KEY_MUTE
KEY_NINE_SEPERATE
KEY_OPEN
KEY_PANNEL_CHDOWN
KEY_PANNEL_CHUP
KEY_PANNEL_ENTER
KEY_PANNEL_MENU
KEY_PANNEL_POWER
KEY_PANNEL_SOURCE
KEY_PANNEL_VOLDOW
KEY_PANNEL_VOLUP
KEY_PANORAMA
KEY_PAUSE
KEY_PCMODE
KEY_PERPECT_FOCUS
KEY_PICTURE_SIZE
KEY_PIP_CHDOWN
KEY_PIP_CHUP
KEY_PIP_ONOFF
KEY_PIP_SCAN
KEY_PIP_SIZE
KEY_PIP_SWAP
KEY_PLAY
KEY_PLUS100
KEY_PMODE
KEY_POWER
KEY_POWEROFF
KEY_POWERON
KEY_PRECH
KEY_PRINT
KEY_PROGRAM
KEY_QUICK_REPLAY
KEY_REC
KEY_RED
KEY_REPEAT
KEY_RESERVED1
KEY_RETURN
KEY_REWIND
KEY_REWIND_
KEY_RIGHT
KEY_RSS
KEY_INTERNET
KEY_RSURF
KEY_SCALE
KEY_SEFFECT
KEY_SETUP_CLOCK_TIMER
KEY_SLEEP
KEY_SOUND_MODE
KEY_SOURCE
KEY_SRS
KEY_STANDARD
KEY_STB_MODE
KEY_STILL_PICTURE
KEY_STOP
KEY_SUB_TITLE
KEY_SVIDEO1
KEY_SVIDEO2
KEY_SVIDEO3
KEY_TOOLS
KEY_TOPMENU
KEY_TTX_MIX
KEY_TTX_SUBFACE
KEY_TURBO
KEY_TV
KEY_TV_MODE
KEY_UP
KEY_VCHIP
KEY_VCR_MODE
KEY_VOLDOWN
KEY_VOLUP
KEY_WHEEL_LEFT
KEY_WHEEL_RIGHT
KEY_W_LINK
KEY_YELLOW
KEY_ZOOM1
KEY_ZOOM2
KEY_ZOOM_IN
KEY_ZOOM_MOVE
KEY_ZOOM_OUT
'''