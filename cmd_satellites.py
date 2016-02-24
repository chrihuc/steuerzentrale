#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table, mdb_read_table_entry
import socket
from socket import error as socket_error
from alarmevents import alarm_event
import paramiko

import MySQLdb as mdb

aes = alarm_event()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class sql_object:
    def __init__(self,name,typ,columns):
        self.name = name
        self.typ = typ
        self.columns = columns

table = sql_object("set_satellites", "Settings", (("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("IP","VARCHAR(45)"),("PORT","INT(11)"),("Type","VARCHAR(45)"),("USER","VARCHAR(45)"),("PASS","VARCHAR(45)"),("command_set","VARCHAR(45)")))

def  get_satellites():
    list = mdb_get_table(constants.sql_tables.satellites.name)
    simplelist = []
    x = None
    for satellite in list:
        x = sputnik(satellite.get("Name"),satellite.get("IP"),satellite.get("PORT"),satellite.get("Type"),satellite.get("USER"),satellite.get("PASS"),satellite.get("command_set"))
        x.attr = satellite
        simplelist.append(x)
    return simplelist

def  get_satellite(name):
    list = mdb_get_table(constants.sql_tables.satellites.name)
    simplelist = []
    x = None
    for satellite in list:
        if satellite.get("Name") == name:
            x = sputnik(satellite.get("Name"),satellite.get("IP"),satellite.get("PORT"),satellite.get("Type"),satellite.get("USER"),satellite.get("PASS"),satellite.get("command_set"))
            x.attr = satellite
    return x

def main():
    sats = satelliten()
    print sats.list_devices()
    print sats.list_commands("Sideb_links")
    print sats.set_device('LightstripSchlafzi','Hell')

class satelliten:
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket_old = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    
    def __init__ (self):
        self.__init_table__()
        self.__check_table__()
    
    def __init_table__(self):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+table.name+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+table.name +"("
                for num, col in enumerate(table.columns):
                    if num == len(table.columns)-1:
                        for co in col:
                            command += co + " "
                        command +=  ");"
                    else:
                        for co in col:
                            command += co + " "                    
                        command +=  ", "
                cur.execute(command)
                results = cur.fetchall()      
        con.close() 
        
    def __check_table__(self):
        for sat in self.list_devices():
            con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
            with con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM "+constants.sql_.DB+"."+table.name+" WHERE Name = '"+sat+"'")
                if cur.fetchone()[0] == 0:
                    sql = 'INSERT INTO '+table.name+' (Name, command_set) VALUES ("'+ str(sat) + '","'+'sat_'+ str(sat) + '")'     
                    cur.execute(sql)
            con.close() 
            
    def __check_table_exists__(self,table):
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+table+"'")
            if cur.fetchone()[0] == 0:       
                command = "CREATE TABLE "+constants.sql_.DB+"."+table +"(`id` int(11) NOT NULL AUTO_INCREMENT, `Name` varchar(50),PRIMARY KEY (`id`));"
                cur.execute(command)
                results = cur.fetchall()      
        con.close()         

    def list_devices(self):
        comands = mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
        liste = []
        for comand in comands:
            if comands.get(comand) == "SATELLITE":
                liste.append(comand)
        #liste.remove("Name")
        return liste    
        
    def list_commands(self,device='alle'):
        liste = [] 
        list_cmds_of = []
        if device == 'alle':
            list_cmds_of = self.list_devices()
        else:
            list_cmds_of.append(device)
        for sates in list_cmds_of:
            cmds_table=mdb_read_table_entry(table.name,sates).get('command_set')
            self.__check_table_exists__(cmds_table)            
            comands = mdb_get_table(cmds_table)
            for comand in comands:
                liste.append(comand.get("Name"))
        return liste        

    def dict_commands(self,device='alle'):
        liste = {}
        itera = 1
        liste[''] = itera
        list_cmds_of = []
        if device == 'alle':
            list_cmds_of = self.list_devices()
        else:
            list_cmds_of.append(device)
        for sates in list_cmds_of:
            cmds_table=mdb_read_table_entry(table.name,sates).get('command_set')
            self.__check_table_exists__(cmds_table)            
            comands = mdb_get_table(cmds_table)
            for comand in comands:
                itera +=1
                liste[comand.get("Name")] = itera                
        return liste        


    def set_device(self, device, commd):   
        satellit=mdb_read_table_entry(table.name,device)
        command = mdb_read_table_entry(satellit.get('command_set'),commd)
        command["Device"]=device
        data = ""
        try:
            satelliten.mysocket_old.sendto(str(command),(satellit.get('IP'),satellit.get('PORT')))
        except:
            pass
        try:
            satelliten.mysocket.settimeout(10)
            satelliten.mysocket.connect((satellit.get('IP'),satellit.get('PORT')))
            satelliten.mysocket.send(str(command))
            data=satelliten.mysocket.recv(1024)
            satelliten.mysocket.close()
        except:
            satelliten.mysocket.close()
        if data  == "True":
            return True
        else:
            return False
             
        
class sputnik:
    mysocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    
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