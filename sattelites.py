#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table
from socket import error as socket_error
from alarmevents import alarm_event
import paramiko

aes = alarm_event()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def  get_sattelites():
    list = mdb_get_table("sattelites")
    simplelist = []
    for sattelite in list:
        x = raspi(sattelite.get("Name"),sattelite.get("IP"),sattelite.get("PORT"),sattelite.get("Type"),sattelite.get("USER"),sattelite.get("PASS"))
        x.attr = sattelite
        simplelist.append(x)
    return simplelist

def main():
    pies = get_sattelites()
    for pi in pies:
        if pi.Type == "sat":
            print pi.reboot()

class raspi:
    def __init__ (self, name, IP, PORT, Type, USER, PASS):
        self.name = name
        self.IP = IP
        self.PORT = PORT
        #Router, sat, server, virt
        self.Type = Type
        self.USER = USER
        self.PASS = PASS

    def send_ssh_cmd(self, cmd_to_execute, text="N/A", tries=5):
        success = False
        count = 0
        while (not success) and (count <= tries):
            count += 1
            try:
                ssh.connect(self.IP, username=self.USER, password=self.PASS)
                #if constants.master:
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
                success = True
            except socket_error as serr:
                success = False
            except: 
                success = False        
        if success:
            aes.new_event(description=self.name + " " + text, prio=0)
        else:
            aes.new_event(description=self.name + " nicht erreichbar", prio=1)
        return success

    def reboot(self):
        return self.send_ssh_cmd("sudo reboot","neugestarted")


if __name__ == '__main__':
    main()  
