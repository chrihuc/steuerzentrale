#!  /usr/bin/python
 
import socket
import base64
import time, datetime
from socket import error as socket_error

def main():
    #tv_remote = remotecontrol('192.168.192.10','192.168.192.26','00:30:1b:a0:2f:05')
    tv_remote_lan = remotecontrol('192.168.192.10','192.168.192.29','00:30:1b:a0:2f:05')
    #tv_remote.authenti()
    tv_remote_lan.authenti()

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

     
    # Key Reference
    # Normal remote keys
     #KEY_0
     #KEY_1
     #KEY_2
     #KEY_3
     #KEY_4
     #KEY_5
     #KEY_6
     #KEY_7
     #KEY_8
     #KEY_9
     #KEY_UP
     #KEY_DOWN
     #KEY_LEFT
     #KEY_RIGHT
     #KEY_MENU
     #KEY_PRECH
     #KEY_GUIDE
     #KEY_INFO
     #KEY_RETURN
     #KEY_CH_LIST
     #KEY_EXIT
     #KEY_ENTER
     #KEY_SOURCE
     #KEY_AD #KEY_PLAY
     #KEY_PAUSE
     #KEY_MUTE
     #KEY_PICTURE_SIZE
     #KEY_VOLUP
     #KEY_VOLDOWN
     #KEY_TOOLS
     #KEY_POWEROFF
     #KEY_CHUP
     #KEY_CHDOWN
     #KEY_CONTENTS
     #KEY_W_LINK #Media P
     #KEY_RSS #Internet
     #KEY_MTS #Dual
     #KEY_CAPTION #Subt
     #KEY_REWIND
     #KEY_FF
     #KEY_REC
     #KEY_STOP
    # Bonus buttons not on the normal remote:
     #KEY_TV
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
