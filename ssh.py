#!  /usr/bin/python

import paramiko
from socket import error as socket_error
from alarmevents import alarm_event    
from classes import myezcontrol

ssh = paramiko.SSHClient()
server = "192.168.192.25"
username="pi"
password="raspberry"
cmd_to_execute="sudo reboot"
restart_kommando= "sudo killall python"
aes = alarm_event()
ezcontrol = myezcontrol('192.168.192.4','admin','Ivenhoe')

def main():
    router = ssh_connection(ip = "192.168.192.1", username = "admin", passwort = "Ivenhoe")
    router.close_firewall("192.168.192.190")

def reboot_pis():
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    server = "192.168.192.24"
    try:
        ssh.connect(server, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        aes.new_event(description="Bettcontrol neugestartet", prio=0)
    except socket_error as serr:
        aes.new_event(description="Bettcontrol nicht erreichbar", prio=1)
    except: 
        pass
    server = "192.168.192.25"
    try:    
        ssh.connect(server, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        aes.new_event(description="TVcontrol neugestartet", prio=0)
    except socket_error as serr:
        aes.new_event(description="TVcontrol nicht erreichbar", prio=1)
    except: 
        pass

def restart_pi(server):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(server, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(restart_kommando)
        aes.new_event(description=server+" neugestartet", prio=0)
    except socket_error as serr:
        aes.new_event(description=server+" nicht erreichbar", prio=1)
    except: 
        pass   

class ssh_connection:
    def __init__(self,ip, username, passwort):
        self.ip = str(ip)
        self.username = str(username)
        self.passwort = str(passwort)

    def open_firewall(self, dev_ip):
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server = self.ip
        try:
            ssh.connect(server, username=self.username, password=self.passwort)
            Kommando1 = "iptables -D FORWARD -s 0/0 -d " + dev_ip + " -j DROP"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(Kommando1)
            Kommando2 = "iptables -D FORWARD -s " + dev_ip + " -d 0/0 -j DROP"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(Kommando2)            
            aes.new_event(description=dev_ip + " Firewall opened", prio=0)
        except socket_error as serr:
            aes.new_event(description=self.ip + " nicht erreichbar", prio=1)
        except: 
            pass

    def close_firewall(self, dev_ip):
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server = self.ip
        try:
            ssh.connect(server, username=self.username, password=self.passwort)
            Kommando1 = "iptables -I FORWARD -s 0/0 -d " + dev_ip + " -j DROP"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(Kommando1)
            Kommando2 = "iptables -I FORWARD -s " + dev_ip + " -d 0/0 -j DROP"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(Kommando2)            
            aes.new_event(description=dev_ip + " Firewall opened", prio=0)
        except socket_error as serr:
            aes.new_event(description=self.ip + " nicht erreichbar", prio=1)
        #except: 
        #    pass        

if __name__ == '__main__':
    main() 
                