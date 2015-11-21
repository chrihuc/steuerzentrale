#!/usr/bin/env python

import constants

import MySQLdb as mdb
from Sonos2Py import sonos
from threading import Timer

sn=sonos()

def main():
    #set_automode(device="Stehlampe", mode="auto")
    print mdb_szene_r("Auto_Mode")

    
def gcm_users_read():
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    dicti = {}
    liste = []
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM gcm_users'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        j = 0
        for row in results:
            for i in range (0,len(row)):
                #print row[i]
                dicti[field_names[i]] = row[i]
            liste.append(dicti)
            dicti = {}
            j = j + 1
        return liste    
    
def mdb_sonos_r(player):
    dicti = {}
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM Sonos WHERE Name = "' + str(player) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               #print row[i]
               dicti[field_names[i]] = row[i]            
        return dicti
        for row in results:
            MasterZone = row[1]
            Pause = row[2]
            Sender = row[3]
            Radio = row[4]   
            TitelNr = row[5]
            Time = row[6]
            PlayListNr = row[7]     
            Volume = row[8]
        return {'Pause':Pause,'Radio':Radio,'Sender':Sender,'TitelNr':TitelNr,'Time':Time,'MasterZone':MasterZone,'PlayListNr':PlayListNr, 'Volume':Volume}
    con.close()  

def mdb_sonos_s(player, Pause, Radio, Sender, TitelNr, Time, MasterZone, Volume):
    if player == sn.WohnZi:
        playern = "WohnZi"
    elif player == sn.Kueche:
        playern = "Kueche"
    elif player == sn.Bad:
        playern = "Bad"
    elif player == sn.SchlafZi:
        playern = "SchlafZi"
    else:
        playern = player
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    if Volume == 'None':
        with con:
            cur = con.cursor()
            sql = "UPDATE Sonos SET MasterZone = '" + str(MasterZone) + "', Pause = '" + str(Pause) + "', Sender = '" + str(Sender) + "', Radio = '" + str(Radio) + "', TitelNr = '" + str(TitelNr) + "', Time = '" + str(Time) + "', Volume = NULL WHERE Name = '" + str(playern) + "'"
            cur.execute(sql)
    else:
        with con:
            cur = con.cursor()
            sql = "UPDATE Sonos SET MasterZone = '" + str(MasterZone) + "', Pause = '" + str(Pause) + "', Sender = '" + str(Sender) + "', Radio = '" + str(Radio) + "', TitelNr = '" + str(TitelNr) + "', Time = '" + str(Time) + "', Volume = '" + str(Volume) + "' WHERE Name = '" + str(playern) + "'" 
            cur.execute(sql)        
    con.close()
    
def setting_s(setting, wert):
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = 'UPDATE Settings SET Value = "' + str(wert) + '" WHERE Name = "'+ str(setting) + '"'
        cur.execute(sql)
    con.close() 
    
def setting_r(setting):
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM Settings WHERE Name = "' + str(setting) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            fname = row[1]
            value = row[2]
    con.close()            
    return value
        
def app_r(name):
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM App WHERE Kommando = "' + str(name) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            fname = row[1]
            value = row[2]
    con.close()            
    return value

def set_automode(device, mode):
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = 'UPDATE Szenen SET '+device+' = "' + str(mode) + '" WHERE Name = "Auto_Mode"'
        cur.execute(sql)
    con.close()             
    

def mdb_hue_s(device, setting):
    #setting must be a dict
    #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = "UPDATE Hue SET hue = '" + str(setting.get("hue")) + "', bri = '" + str(setting.get("bri")) + "', sat = '" + str(setting.get("sat")) + "', an = '" + str(setting.get("an")) + "' WHERE Name = '" + device +"'"
        cur.execute(sql) 
    con.close()
    
def mdb_fern_r(Table, Knopf):
    setting_ = setting_r("Status")
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    szenen = []
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT Szene FROM ' + str(Table)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            for i in range (0,len(row)):   
               szenen.append(row[i])
    if setting_ in szenen:
        pass
    else:
        setting_ = "Rest"
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + str(Table) +' WHERE Szene = "' + str(setting_) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               #print row[i]
               dicti[field_names[i]] = row[i]  
    con.close()               
    return dicti.get(Knopf) 

def mdb_fern_r_neu(Setting, Table, Knopf):
    setting_ = setting_r(Setting)
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    szenen = []
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT Szene FROM ' + str(Table)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            for i in range (0,len(row)):   
               szenen.append(row[i])
    if setting_ in szenen:
        pass
    else:
        setting_ = "Rest"
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + str(Table) +' WHERE Szene = "' + str(setting_) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               #print row[i]
               dicti[field_names[i]] = row[i]
        if ((dicti.get("NeuerStatus") <> "") and (str(dicti.get("NeuerStatus")) <> "None")):
            try:
                if type(eval(dicti.get("NeuerStatus"))) == list:
                    kommandos = eval(dicti.get("NeuerStatus"))
                else:
                    kommandos = [dicti.get("NeuerStatus")]
            except NameError as serr:
                kommandos = [dicti.get("NeuerStatus")]
            try:
                if type(eval(dicti.get("Status_Delay"))) == list:
                    delays = eval(dicti.get("Status_Delay"))
                else:
                    delays = [dicti.get("Status_Delay")]
            except NameError as serr:
                delays = [dicti.get("Status_Delay")]                 
            for index, kommando in enumerate(kommandos):
                #lgd.log(" Wait " + str(delays[index]) + " szene " + str(kommando))
                StatusFolgt = Timer(float(delays[index]), set_status, [Setting, str(kommando)])
                StatusFolgt.start() 
    con.close()                
    return dicti.get(Knopf)        

def set_status(Setting, neuer_Status):
        setting_s(Setting, neuer_Status)
        
def mdb_fern_schluessel_r(schlue_c, schlue_s, schlue_c_n, schlue_s_n):
    setting_ = setting_r("Status")
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    szenen = []
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM Fern_Schluessel WHERE Status = "' + str(setting_) +'" and Schluessel_Christoph = "' + str(schlue_c) +'" and Schluessel_Sabina = "' + str(schlue_s) +'" and Schluessel_Christoph_neu = "' + str(schlue_c_n) +'" and Schluessel_Sabina_neu = "' + str(schlue_s_n) + '"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               #print row[i]
               dicti[field_names[i]] = row[i]            
    con.close()    
    return dicti.get("Szene")


def mdb_marantz_s(name, setting):
    #setting must be a dict
    #{'Treble': '7', 'Bass': '2', 'Power': 'True', 'Mute': 'False', 'Attenuate': 'False', 'Volume': '-25', 'Source': '11'}
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = "UPDATE Marantz SET Power = '" + str(setting.get("Power")) + "', Volume = '0" + str(setting.get("Volume")) + "', Source = '" + str(setting.get("Source")) + "', Mute = '" + str(setting.get("Mute")) + "' WHERE Name = '" + name +"'"
        cur.execute(sql) 
    con.close()        
        

def mdb_sideb_s(name, setting):
    #setting must be a dict
    #{'hue': '7', 'bri': '2', 'sat': 'True', 'on': 'False'}
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    with con:
        cur = con.cursor()
        sql = "UPDATE Sideboard SET rot = '" + str(setting.get("rot")) + "', gruen = '" + str(setting.get("gruen")) + "', blau = '" + str(setting.get("blau")) + "' WHERE Name = '" + name +"'"
        cur.execute(sql)     
    con.close()        

## alle mit dicti:
def mdb_get_dicti(db, name):
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM ' + db + ' WHERE Name = "' + str(name) +'"'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            for i in range (0,len(row)):
               dicti[field_names[i]] = row[i]            
    con.close()    
    return dicti       

def mdb_sideb_r(name):
    return mdb_get_dicti('Sideboard', name) 

def mdb_marantz_r(name):
    return mdb_get_dicti('Marantz', name) 
        
def mdb_ls_sz_r(name):
    return mdb_get_dicti('LightstrSchlafzi', name)    

def hue_autolicht(name):
    return mdb_get_dicti('hue_autolicht', name)  
    
def mdb_szene_r(name):
    return mdb_get_dicti('Szenen', name)       
        
def mdb_hue_r(name):
    return mdb_get_dicti('Hue', name)

def mdb_tspled_r(name):
    return mdb_get_dicti('TuerSPiLED', name) 
    
def settings_r():
    con = mdb.connect('192.168.192.10', 'python_user', 'python', 'XS1DB')
    dicti = {}
    with con:
        cur = con.cursor()
        sql = 'SELECT * FROM Settings'
        cur.execute(sql)
        results = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        for row in results:
            dicti[row[1]] = row[2]            
    con.close()    
    return dicti        
        
if __name__ == '__main__':
    main()    