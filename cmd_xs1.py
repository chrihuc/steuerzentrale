#!/usr/bin/env python

import constants

import urllib2
from mysql_con import mdb_read_table_entry,set_val_in_szenen

def main():
    ezcontrol = myezcontrol(constants.xs1_.IP) 
    ezcontrol.set_device("Esszimmer", "100")
    print ezcontrol.list_commands()

#def dimmen(device):
    #setting_s(device, "heller")
    #while str(setting_r(device)) <> 'fixed':
        #Helligkeit = ezcontrol.GetSwitch(device)
        #if (Helligkeit == "100.0"):
            #setting_s(device, "dunkler")
        #elif (Helligkeit == "0.0"):
            #setting_s(device, "heller")
        #if str(setting_r(device)) == "heller":
            #n_Helligkeit = str(float(Helligkeit)+10)
        #else:
            #n_Helligkeit = str(float(Helligkeit)-10)
        #ezcontrol.SetSwitch(device, str((n_Helligkeit)))
        #time.sleep(1.5)

#def xs1_set_szene(device, szene):
    #if szene in ["man", "auto"]:
        #mysql_con.set_automode(device=device, mode=szene)
        #return
    #if szene == "dimmen":
        #if str(setting_r(device)) <> 'fixed':
            #setting_s(device, "fixed")
        #else:
            #dimmen(device)
        #return
    #if szene == str(-1):
        #if ezcontrol.GetSwitch(str(device)) > "0.0":
            #ezcontrol.SetSwitch(str(device), "0.0")
        #else:
            #ezcontrol.SetSwitch(str(device), "100.0")
    #else:
        #ezcontrol.SetSwitch(str(device), str(szene))

class myezcontrol:
    def __init__(self,ip):
        self.data = []
        self.ip_add = str(ip)
        
    def SetSwitch(self,Switch,Wert):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&value=""" + str(Wert)
        f = urllib2.urlopen(body)
        f.close()

    def SetSwitchFunction(self,Switch,Function):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&Function=""" + str(Function)
        f = urllib2.urlopen(body)     
        f.close()
        
    def GetSwitch(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_actuator&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        f.close() 
        return Wert
        
    def GetBattery(self,name):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(name)
        f = urllib2.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        decoded = json.loads(html)
        battery = decoded['sensor']['state']
        status = battery[0]
        dict = {'battery':battery}
        f.close()
        return status        
        
    def GetSensor(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        f.close()
        return Wert     

    def GetSensor_neu(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(Switch)
        f = urllib2.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"state":')
        Wert = html [position1+9:position2-4]
        f.close()
        return Wert       
    
    def list_commands(self):
        #comands = mdb_get_table(table.name)
        liste = ["toggle",0,100]
        #for comand in comands:
            #liste.append(comand.get("Name"))
        #liste.remove("Name")
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
        comands = mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
        liste = []
        for comand in comands:
            if comands.get(comand) == "XS1":
                liste.append(comand)
        #liste.remove("Name")
        return liste
    
    def set_device(self, device, commd):
        try:
            if commd in ["man", "auto"]:
                set_val_in_szenen(device=device, szene="Auto_Mode", value=commd)
            if commd == str(-1) or commd == "toggle":
                if self.GetSwitch(str(device)) > "0.0":
                    self.SetSwitch(str(device), "0.0")
                    set_val_in_szenen(device=device, szene="Value", value=0)
                else:
                    self.SetSwitch(str(device), "100.0")
                    set_val_in_szenen(device=device, szene="Value", value=100)
            else:
                self.SetSwitch(str(device), str(commd))  
                set_val_in_szenen(device=device, szene="Value", value=commd)
            return True
        except:
            return False
            
if __name__ == '__main__':
    main()  