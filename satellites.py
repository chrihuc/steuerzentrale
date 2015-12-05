#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table
from socket import socket, AF_INET, SOCK_DGRAM
from socket import error as socket_error
from alarmevents import alarm_event
import paramiko

aes = alarm_event()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def  get_satellites():
    list = mdb_get_table("satellites")
    simplelist = []
    for satellite in list:
        x = sputnik(satellite.get("Name"),satellite.get("IP"),satellite.get("PORT"),satellite.get("Type"),satellite.get("USER"),satellite.get("PASS"),satellite.get("command_set"))
        x.attr = satellite
        simplelist.append(x)
    return simplelist

def  get_satellite(name):
    list = mdb_get_table("satellites")
    simplelist = []
    for satellite in list:
        if satellite.get("Name") == name:
            x = sputnik(satellite.get("Name"),satellite.get("IP"),satellite.get("PORT"),satellite.get("Type"),satellite.get("USER"),satellite.get("PASS"),satellite.get("command_set"))
            x.attr = satellite
    return x

def main():
    pies = get_satellites()
    for pi in pies:
        if pi.Type == "sat":
            print pi.reboot()

class sputnik:
    mysocket = socket( AF_INET, SOCK_DGRAM )
    
    def __init__ (self, name, IP, PORT, Type, USER, PASS, command_set):
        self.name = name
        self.IP = IP
        self.PORT = PORT
        #Router, sat, server, virt
        self.Type = Type
        self.USER = USER
        self.PASS = PASS
        self.command_set = command_set
        self.no_of_hb = 0
        self.no_of_lb = 0

    def send_ssh_cmd(self, cmd_to_execute, text="N/A", tries=10):
        success = False
        count = 0
        while (not success) and (count <= tries):
            count += 1
            try:
                ssh.connect(self.IP, username=self.USER, password=self.PASS)
                if constants.redundancy_.master:
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
    
    def kill_python(self):
        return self.send_ssh_cmd("sudo killall python","python killed")  
    
    def open_fw(self, dev_ip):
        return self.send_ssh_cmd("iptables -D FORWARD -s 0/0 -d " + dev_ip + " -j DROP", "Firewall opened 1 " +dev_ip)
        return self.send_ssh_cmd("iptables -D FORWARD -s " + dev_ip + " -d 0/0 -j DROP", "Firewall opened 2 " +dev_ip)   

    def close_fw(self, dev_ip):
        return self.send_ssh_cmd("iptables -I FORWARD -s 0/0 -d " + dev_ip + " -j DROP", "Firewall closed 1 " +dev_ip)
        return self.send_ssh_cmd("iptables -I FORWARD -s " + dev_ip + " -d 0/0 -j DROP", "Firewall closed 2 " +dev_ip) 

    def send_udp_cmd(self, command):
        if constants.redundancy_.master:
            sputnik.mysocket.sendto(str(command),(self.IP,self.PORT))

if __name__ == '__main__':
    main()  
