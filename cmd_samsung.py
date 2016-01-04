#!  /usr/bin/python
 
import constants 
 
import socket
import base64
import time
from socket import error as socket_error

from mysql_con import mdb_read_table_entry,set_val_in_szenen

def main():
    rem = TV()
    print rem.list_commands()
    print rem.list_devices()
    print rem.set_device("TV","KEY_VOLUP")
    #tv_remote.authenti()
    #tv_remote_lan.authenti()

class remotecontrol:
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
    
    # Function to send keys
    def sendKey(self, skey):
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.settimeout(10)
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
             messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
             part3 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
             sock.send(part3)
             time.sleep(0.3)
         sock.close()
         return True
     except socket_error as serr:
        return False   

class TV:
    def __init__(self):
        self.tv_remote = remotecontrol('192.168.192.10','192.168.192.26','00:30:1b:a0:2f:05')
        self.tv_remote_lan = remotecontrol('192.168.192.10','192.168.192.29','00:30:1b:a0:2f:05')         
        
    def set_device(self,device, commd):
        if commd in ["man", "auto"]:
            set_val_in_szenen(device=device, szene="Auto_Mode", value=commd)        
        if self.tv_remote_lan.sendKey([str(commd)]) or self.tv_remote.sendKey([str(commd)]):
            set_val_in_szenen(device=device, szene="Value", value=commd)
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
    # Bonus buttons not on the normal remote:
        liste += ["KEY_TV"]
        return liste
     
    def list_devices(self):
        comands = mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
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

if __name__ == '__main__':
    main()
