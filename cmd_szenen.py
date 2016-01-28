# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:21:24 2016

@author: christoph
"""

#!/usr/bin/env python

import constants

from mysql_con import mdb_get_table, mdb_read_table_column, mdb_read_table_entry, settings_r

from cmd_sonos import sonos
from cmd_xs1 import myezcontrol
from cmd_hue import hue_lights
from cmd_samsung import TV
from cmd_satellites import satelliten
from alarmevents import alarm_event

xs1 = myezcontrol(constants.xs1_.IP)
hue = hue_lights()
sn = sonos()
tv = TV()
sat = satelliten()
xs1_devs = xs1.list_devices()
hue_devs = hue.list_devices()
sns_devs = sn.list_devices()
tvs_devs = tv.list_devices()
sat_devs = sat.list_devices()
aes = alarm_event()



def main():
    scenes = szenen()
    print scenes.list_commands()
    
class szenen:
    def __init__ (self):
        pass
    
    def list_commands(self,gruppe='alle'):    
        table = mdb_get_table(constants.sql_tables.szenen.name)
        liste = []
        if gruppe == "alle":
            for szene in table:
                if szene.get("Gruppe") <>"Intern":
                    liste.append(szene.get("Name"))
        else:
                if szene.get("Gruppe") <>"Intern" and szene.get("Gruppe") == gruppe:
                    liste.append(szene.get("Name"))            
        return liste

    def execute(self, szene):
        szene_dict = mdb_read_table_entry(constants.sql_tables.szenen.name, szene)
        #check bedingung
        bedingungen = {}
        erfuellt = True
        if str(szene_dict.get("Bedingung")) <> "None":
            bedingungen = eval(szene_dict.get("Bedingung"))    
            erfuellt = True
        settings = settings_r()
        for bedingung in bedingungen:
            try:
                groesser = bedingungen.get(bedingung).find('>')
                kleiner = bedingungen.get(bedingung).find('<')
                if groesser >-1 and kleiner >-1:
                    schwelle_u = float(bedingungen.get(bedingung)[groesser+1:kleiner])
                    if float(settings.get(bedingung)) <= schwelle_u:
                        erfuellt = False
                    schwelle_o = float(bedingungen.get(bedingung)[kleiner+1:len(bedingungen.get(bedingung))])
                    if float(settings.get(bedingung)) >= schwelle_o:
                        erfuellt = False    
                elif groesser >-1:
                    schwelle = float(bedingungen.get(bedingung)[groesser+1:len(bedingungen.get(bedingung))])
                    if float(settings.get(bedingung)) <= schwelle:
                        erfuellt = False                     
                elif kleiner >-1:
                    schwelle = float(bedingungen.get(bedingung)[kleiner+1:len(bedingungen.get(bedingung))])
                    if float(settings.get(bedingung)) >= schwelle:
                        erfuellt = False        
                else:
                    if not(str(settings.get(bedingung)) in bedingungen.get(bedingung)):
                        erfuellt = False
            except Exception as e:
                if not(str(settings.get(bedingung)) in bedingungen.get(bedingung)):
                    erfuellt = False  
        if erfuellt:
            if str(szene_dict.get("Beschreibung")) in ['None','']:
                aes.new_event(description="Szenen: " + szene, prio=eval(szene_dict.get("Prio")), karenz = 0.03)
            else:
                aes.new_event(description= str(szene_dict.get("Beschreibung")), prio=eval(szene_dict.get("Prio")), karenz = 0.03)                    

if __name__ == '__main__':
    main()      