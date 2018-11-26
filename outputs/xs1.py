#!/usr/bin/env python

import constants

import sys
if sys.version_info >= (3, 0):
    import urllib.request
else:
    import urllib2

import json
from database import mysql_connector

from tools import toolbox
#toolbox.log('debug on')

# TODO Tests split adress from hks


class XS1:
    def __init__(self,ip=constants.xs1_.IP):
        self.data = []
        self.ip_add = str(ip)

    def SetSwitch(self,Switch,Wert):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&value=""" + str(Wert)
        f = urllib.request.urlopen(body)
        f.close()

    def SetSwitchFunction(self,Switch,Function):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=set_state_actuator&name=""" + str(Switch) + """&Function=""" + str(Function)
        toolbox.log(body)
        f = urllib.request.urlopen(body)
        f.close()

    def GetSwitch(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_actuator&name=""" + str(Switch)
        f = urllib.request.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        f.close()
        return Wert

    def GetBattery(self,name):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(name)
        f = urllib.request.urlopen(body)
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
        f = urllib.request.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"newvalue":')
        Wert = html [position1+9:position2-4]
        f.close()
        return Wert

    def GetSensor_neu(self,Switch):
        url = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_state_sensor&name=""" + str(Switch)
        f = urllib.request.urlopen(url)
        html = f.read()
        position1 = html.find ('"value":')
        position2 = html.find ('"state":')
        Wert = html [position1+9:position2-4]
        f.close()
        return Wert

    def GetTimer(self,name):
        body = """http://""" + self.ip_add + """/control?user=""" + self.usern + """&pwd=""" + self.password + """&cmd=get_config_timer&name=""" +name + """&callback=cname"""
        f = urllib.request.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        decoded = json.loads(html)
        enabled = decoded['timer']['type']
        number = decoded['timer']['number']
        weekdays = decoded['timer']['weekdays']
        time = decoded['timer']['time']
        random = decoded['timer']['random']
        offset = decoded['timer']['offset']
        earliest = decoded['timer']['earliest']
        latest = decoded['timer']['latest']
        actuator = decoded['timer']['actuator']
        dict = {'enabled':enabled,'number':number,'weekdays':weekdays,'time':time,'random':random,'offset':offset,'earliest':earliest,'latest':latest,'actuator':actuator}
        return dict

    def SetTimer(self,enable,number,name,weekdays,hour,minute,sec,offset,random,earliest,latest,actname,function):
        body1 = """http://""" + self.ip_add + """/control?user=""" + self.usern + """&pwd=""" + self.password
        body2 = """&v=16&cmd=SET_CONFIG_TIMER&number=""" + number + """&type="""+ enable +"""&name="""+ name
        body3 = """&weekdays=""" + weekdays + """&hour=""" + hour + """&min=""" + minute + """&sec=""" + sec
        body4 = """&offset=""" + offset + """&random=""" + random + """&earliest=""" + earliest + """&latest=""" + latest
        body5 = """&actuator.name=""" + actname + """&actuator.function=""" + function + """&callback=JSON133"""
        body = body1 + body2 + body3 + body4 + body5
        f = urllib.request.urlopen(body)

    def list_commands(self):
        #comands = mdb_get_table(table.name)
        liste = ['Umschalten',0,100,15,17,22.5,'func_1','func_2','func_3','func_4']
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
        comands = mysql_connector.mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
        liste = []
        for comand in comands:
            if comands.get(comand) == "XS1":
                liste.append(comand)
        #liste.remove("Name")
        return liste

    def list_sensors(self):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_list_sensors"""
        f = urllib.request.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        decoded = json.loads(html)
        return decoded

    def check_batteries(self):
        sensors = self.list_sensors()
        for sensor in sensors['sensor']:
            if 'batterylow' in sensor['state']:
                print(sensor['name'])

    def list_actors(self):
        body = """http://""" + self.ip_add + """/control?callback=cname&cmd=get_list_actuators"""
        f = urllib.request.urlopen(body)
        html = f.read()
        html = html[5:]
        html = html.replace(" ", "")
        html = html.replace("(", "")
        html = html.replace(")", "")
        actors = json.loads(html)
        act_list = []
        for actor in actors['actuator']:
            act_list.append(actor['name'])
        return act_list

    def set_device(self, device, commd):
        try:
            if commd == str(-1) or commd == "toggle":
                if self.GetSwitch(str(device)) > "0.0":
                    self.SetSwitch(str(device), "0.0")
                    value=0
                else:
                    self.SetSwitch(str(device), "100.0")
                    value=100
            elif 'func' in str(commd):
                self.SetSwitchFunction(str(device), str(commd)[5:])
            else:
                self.SetSwitch(str(device), str(commd))
            return True
        except:
            return False
