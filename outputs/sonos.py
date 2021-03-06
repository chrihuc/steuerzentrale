#!/usr/bin/env python
# -*- coding: utf-8 -*-

import soco
import wave
import contextlib
import subprocess
import pwd, os
import threading

from alarm_event_messaging import alarmevents as aevs
aes = aevs.AES()

import constants
from tools import decorators

from random import choice

import sys
if sys.version_info >= (3, 0):
    from urllib.parse import quote
    import http.client
else:
    from urllib import quote


import requests
import time
from time import localtime,strftime
from datetime import date
import MySQLdb as mdb
from database import mysql_connector
from outputs import cron

from tools import toolbox

#AVTransport (GetTransportInfo, SetPause, SetPlay, CombineZones, StreamInput, ClearZones, AddTrack, RemoveTrack, GetPosition, GetPositionInfo, Seek, ActivateList, ClearList, PlayList (defect), PlayListNr)
#RenderingControl (SetMute, GetVolume, SetVolume)
# TODO Tests split adress from hks

crn = cron.Cron()

table = constants.sql_object("out_Sonos", "Outputs",(("Id","INT(11)","PRIMARY KEY","AUTO_INCREMENT"),("Name","VARCHAR(45)"),("MasterZone","VARCHAR(45)"),("Pause","INT(4)"),("Sender","VARCHAR(300)"),("Radio","INT(4)"),("TitelNr","VARCHAR(45)"),("Time","VARCHAR(45)"),("PlayListNr","VARCHAR(45)"),("Volume","VARCHAR(45)")))

#sonos_ezcont = {str(sn.WohnZi):'Sonos_Wohnzi',str(sn.Kueche):'Sonos_Kueche',str(sn.Bad):'Sonos_Bad',str(sn.SchlafZi):'Sonos_Schlafzi'}
#sonos_szenen = {str(sn.WohnZi):'WohnZi',str(sn.Kueche):'Kueche',str(sn.Bad):'Bad',str(sn.SchlafZi):'SchlafZi'}

#Envelope for all AVTrans actions the same
def Envelope(self, Player, body, SOAPAction):
    blen = len(body.encode())
    requestor = http.client.HTTPConnection(Player, self.SERVER_PORT)
    requestor.putrequest("POST", "/MediaRenderer/AVTransport/Control HTTP/1.1")
    requestor.putheader("HOST", Player)
    requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
    requestor.putheader("Content-Length", str(blen))
    requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:" + SOAPAction)
    requestor.endheaders()
    requestor.send(body.encode())
    status = requestor.getresponse()
    reply_body = status.read()
    return reply_body

#Envelope for all RendCont actions the same
def EnvelopeRC(self, Player, body, SOAPAction):
    blen = len(body.encode())
    requestor = http.client.HTTPConnection(Player, self.SERVER_PORT)
    requestor.putrequest("POST", "/MediaRenderer/RenderingControl/Control HTTP/1.1")
    requestor.putheader("Host", Player)
    requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
    requestor.putheader("Content-Length", str(blen))
    requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:" + SOAPAction)
    requestor.endheaders()
    requestor.send(body.encode())
    status = requestor.getresponse()
    reply_body = status.read()
    return reply_body

def send_command(self, player, endpoint, action, body):
    headers = {
        'Content-Type': 'text/xml',
        'SOAPACTION': action
    }
    SOAP_TEMPLATE = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>{body}</s:Body></s:Envelope>'
    soap = SOAP_TEMPLATE.format(body=body)
    r = requests.post('http://' + player + ':1400' + endpoint, data=soap, headers=headers)
    return r.content

def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if somepredicate(*args, **kwargs): return True
    time.sleep(period)
  return False


def play_wav(input_para):
    location = constants.installation_folder + '/media/'
    if ('.wav' in input_para) or ('.mp3' in input_para):
        location = location + input_para
    else:
        subprocess.call(["espeak", "-w " + location + "texttosonos.wav", "-a140", "-vmb-de6", "-p40", "-g0", "-s110", "Ansage " + input_para])
        location = location + 'texttosonos.wav'
    os.system("play " + location)
#    os.system("su -m chris -c 'play " + location + "'")


class Sonos:

    Status = {}

    def __init__(self):
        # Workaround
        self.WohnZi = "192.168.192.201"
        self.SchlafZi = "192.168.192.202"
        self.Bad = "192.168.192.203"
        self.Keller = "192.168.192.204"
        self.Kueche = "192.168.192.205"
        self.DG = "192.168.192.206"
        self.Kizi = "192.168.192.207"        
        self.Names = {self.SchlafZi:"SchlafZi", self.Bad:"Bad", self.WohnZi:"WohnZi", self.Kueche:"Kueche",
                      self.Kizi:"Kinderzimmer", self.DG:"Dachgeschoss", self.Keller:"Hobbyraum"}
        
        # deprecated
        self.Devices = {'V00WOH1RUM1AV11':self.WohnZi,'V00KUE1RUM1AV11':self.Kueche,'V01BAD1RUM1AV11':self.Bad,'V01SCH1RUM1AV11':self.SchlafZi}

        # deprecated
        self.SchlafZiZone = "RINCON_000E5830220001400"
        self.BadZone = "RINCON_000E583138BA01400"
        self.WohnZiZone = "RINCON_000E58232A2601400"
        self.KuecheZone = "RINCON_000E58CB9E3E01400"
        self.Zones = [self.SchlafZiZone, self.BadZone, self.WohnZiZone, self.KuecheZone]
#        self.sonos_zonen = {str(self.WohnZi):self.WohnZiZone,str(self.Kueche):self.KuecheZone,str(self.Bad):self.BadZone,str(self.SchlafZi):self.SchlafZiZone}
        self.Devices_neu = {'V00WOH1RUM1AV11':'Wohnzimmer','V00KUE1RUM1AV11':u'K\xfcche','V01BAD1RUM1AV11':'Bad','V01SCH1RUM1AV11':'Schlafzimmer',
                            'Vm1ZIM1RUM1AV11':'Hobbyraum','V01KID1RUM1AV11':'Kinderzimmer'}

        self.SERVER_PORT = 1400
        self.VOLUME = 0
        self.PLAYLISTS = {}
        
        self.devices = set()
        self.list_devices()
        

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

    def socoDiscover(self):
        if len(self.devices) == 0: 
            self.devices = soco.discover()
            if not self.devices:
                aes.new_event(description="Soco discover not working", prio=7)
                self.devices = set()
                for ip in self.Names.keys():
                    if toolbox.ping(ip):
                        newP = soco.SoCo(ip)
                        #print(newP)
                        self.devices.add(newP)
            else:
                aes.new_event(description="Soco discover working again", prio=7)                        
        return self.devices


    def get_addr(self,hks):
        """
        translates hks haus kennzeichen system in ip, uid and p_name
        """
        players = list(self.socoDiscover())
        if hks in self.Devices_neu:
            p_name = self.Devices_neu[hks]
        else:
            p_name = hks
        for player in players:
            if player.player_name == p_name:
                ip = player.ip_address
                uid = player.uid
                return player, ip, uid, p_name

    def get_player(self,uid):
        players = list(self.socoDiscover())
        for player in players:
            if player.uid == uid:
                return player

    def get_zones(self):
        players = list(self.socoDiscover())
        zones = []
        for player in players:
            zones.append(player.uid)
        return zones

    def Envelope(self, Player, body, SOAPAction):
        blen = len(body.encode())
        requestor = http.client.HTTPConnection(Player, self.SERVER_PORT)
        requestor.putrequest("POST", "/MediaRenderer/AVTransport/Control HTTP/1.1")
        requestor.putheader("HOST", Player)
        requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
        requestor.putheader("Content-Length", str(blen))
        requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:" + SOAPAction)
        requestor.endheaders()
        requestor.send(body.encode())
        status = requestor.getresponse()
        reply_body = status.read()
        return reply_body

#AVTransport (GetTransportInfo, SetPause, SetPlay, CombineZones, ClearZones, AddTrack, RemoveTrack, GetPosition, GetPositionInfo, Seek, ActivateList)

    def GetTransportInfo(self, Player):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:GetTransportInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            /u:GetTransportInfo>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "AVTransport:1#GetTransportInfo"
        return Envelope(self, Player, body, SOAPAction)

    def SetPause(self, Player):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            </u:Pause>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "AVTransport:1#Pause"
        return self.Envelope(Player, body, SOAPAction)

    def SetPlay(self, Player):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            <Speed>1</Speed>
            </u:Play>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "AVTransport:1#Play"
        Envelope(self, Player, body, SOAPAction)

    @decorators.deprecated
    def CombineZones(self,Player,Zone):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
            <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            <CurrentURI>x-rincon:""" + Zone + """</CurrentURI>
            <CurrentURIMetaData></CurrentURIMetaData>
            </u:SetAVTransportURI></s:Body></s:Envelope>"""
        SOAPAction = "AVTransport:1#SetAVTransportURI"
        Envelope(self, Player, body, SOAPAction)

    def StreamInput(self,Player,Zone):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
            <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            <CurrentURI>x-rincon-stream:""" + Zone + """</CurrentURI>
            <CurrentURIMetaData></CurrentURIMetaData>
            </u:SetAVTransportURI>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "AVTransport:1#SetAVTransportURI"
        Envelope(self, Player, body, SOAPAction)

    def ClearZones(self,Player):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
            <u:BecomeCoordinatorOfStandaloneGroup xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
            <InstanceID>0</InstanceID>
            </u:BecomeCoordinatorOfStandaloneGroup>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "AVTransport:1#BecomeCoordinatorOfStandaloneGroup"
        Envelope(self, Player, body, SOAPAction)

    def AddTrack(self, Player, Position, File):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>
                    <u:AddURIToQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <EnqueuedURI>x-file-cifs:""" + File + """</EnqueuedURI>
                    <EnqueuedURIMetaData></EnqueuedURIMetaData>
                    <DesiredFirstTrackNumberEnqueued>""" + Position + """</DesiredFirstTrackNumberEnqueued>
                    <EnqueueAsNext>1</EnqueueAsNext>
                    </u:AddURIToQueue></s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#AddURIToQueue"
        Envelope(self, Player, body, SOAPAction)

    def PlayList(self, Player, List):
        List = "file:///jffs/settings/savedqueues.rsq#1"
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>
                    <u:AddURIToQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <EnqueuedURI>""" + List + """</EnqueuedURI>
                    <EnqueuedURIMetaData></EnqueuedURIMetaData>
                    <DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued>
                    <EnqueueAsNext>1</EnqueueAsNext>
                    </u:AddURIToQueue></s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#AddURIToQueue"
        Envelope(self, Player, body, SOAPAction)

    def PlayListNr(self, Player, ListNr):
        List = "file:///jffs/settings/savedqueues.rsq#1"
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>
                    <u:AddURIToQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <EnqueuedURI>file:///jffs/settings/savedqueues.rsq#""" + ListNr + """</EnqueuedURI>
                    <EnqueuedURIMetaData></EnqueuedURIMetaData>
                    <DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued>
                    <EnqueueAsNext>1</EnqueueAsNext>
                    </u:AddURIToQueue></s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#AddURIToQueue"
        return Envelope(self, Player, body, SOAPAction)

    def SaveList(self, Player, List, ListNr):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:SaveQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <Title>""" + List + """</Title>
                    <ObjectID>SQ:""" + str(ListNr) + """</ObjectID>
                    </u:SaveQueue>
                    </s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#SaveQueue"
        return Envelope(self, Player, body, SOAPAction)

    def RemoveTrack(self, Player, TrackNr):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <s:Body>
                <u:RemoveTrackFromQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                <InstanceID>0</InstanceID>
                <ObjectID>Q:0/""" + TrackNr + """</ObjectID>
                <UpdateID>0</UpdateID>
                </u:RemoveTrackFromQueue>
                </s:Body>
                </s:Envelope>"""
        SOAPAction = "AVTransport:1#RemoveTrackFromQueue"
        Envelope(self, Player, body, SOAPAction)

    def GetPosition(self, Player):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID></u:GetPositionInfo></s:Body></s:Envelope>"""
        SOAPAction = "AVTransport:1#GetPositionInfo"
        reply_body = Envelope(self, Player, body, SOAPAction)
        Track1 = reply_body.find ('<Track>',0)
        Track2 = reply_body.find ('</Track>',0)
        Position = []
        Position.append (reply_body [Track1+7:Track2])
        RelTime1 = reply_body.find ('<RelTime>',0)
        RelTime2 = reply_body.find ('</RelTime>',0)
        Position.append (reply_body [RelTime1+9:RelTime2])
        return Position

    def GetPositionInfo2(self, Player):
        TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
        GET_CUR_TRACK_ACTION = '"urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo"'
        GET_CUR_TRACK_BODY = '<u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID></u:GetPositionInfo>'
        response = send_command(self, Player, TRANSPORT_ENDPOINT, GET_CUR_TRACK_ACTION, GET_CUR_TRACK_BODY)
        #body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         #       <s:Body>
         #       <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
         #       <InstanceID>0</InstanceID>
         #       </u:GetPositionInfo>
         #       </s:Body>
         #       </s:Envelope>"""
         # removed: <Channel>Master</Channel>
        #SOAPAction = "AVTransport:1#GetPositionInfo"
        return response

    def GetPositionInfo(self, Player):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <s:Body>
                <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                <InstanceID>0</InstanceID>
                </u:GetPositionInfo>
                </s:Body>
                </s:Envelope>"""
        SOAPAction = "AVTransport:1#GetPositionInfo"
        return Envelope(self, Player, body, SOAPAction)

    def Seek(self, Player, What, Position):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <s:Body>
                <u:Seek xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                <InstanceID>0</InstanceID>
                <Unit>""" + What + """</Unit>
                <Target>""" + str(Position) + """</Target>
                </u:Seek>
                </s:Body>
                </s:Envelope>"""
        SOAPAction = "AVTransport:1#Seek"
        Envelope(self, Player, body, SOAPAction)

    def ActivateList(self, Player, ZoneController):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <CurrentURI>x-rincon-queue:""" + ZoneController + """#0</CurrentURI>
                    <CurrentURIMetaData>
                    </CurrentURIMetaData>
                    </u:SetAVTransportURI>
                    </s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#SetAVTransportURI"
        Envelope(self, Player, body, SOAPAction)

    def setRadio(self, Player, Radio):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    <CurrentURI>""" + Radio + """</CurrentURI>
                    <CurrentURIMetaData></CurrentURIMetaData>
                    </u:SetAVTransportURI>
                    </s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#SetAVTransportURI"
        Envelope(self, Player, body, SOAPAction)

    def ClearList(self, Player):
        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:RemoveAllTracksFromQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                    <InstanceID>0</InstanceID>
                    </u:RemoveAllTracksFromQueue>
                    </s:Body>
                    </s:Envelope>"""
        SOAPAction = "AVTransport:1#RemoveAllTracksFromQueue"
        Envelope(self, Player, body, SOAPAction)

#RenderingControl (SetMute, GetVolume, SetVolume)

    def SetMute(self, Player,wert):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:SetMute xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
            <InstanceID>0</InstanceID>
            <Channel>Master</Channel>
            <DesiredMute>""" + str(wert) + """</DesiredMute>
            </u:SetMute>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "RenderingControl:1#SetMute"
        EnvelopeRC(self, Player, body, SOAPAction)

    def GetVolume(self, Player):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:GetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
            <InstanceID>0</InstanceID>
            <Channel>Master</Channel>
            </u:GetVolume>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "RenderingControl:1#GetVolume"
        reply_body = EnvelopeRC(self, Player, body, SOAPAction)
        position1 = reply_body.find ('<CurrentVolume>')
        position2 = reply_body.find ('</CurrentVolume>')
        VOLUME = int(reply_body [position1+15:position2])
        return VOLUME

    def SetVolume(self, Player, VOLUME):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
            <InstanceID>0</InstanceID>
            <Channel>Master</Channel>
            <DesiredVolume>""" + str(VOLUME) + """</DesiredVolume>
            </u:SetVolume>
            </s:Body>
            </s:Envelope>"""
        SOAPAction = "RenderingControl:1#SetVolume"
        EnvelopeRC(self, Player, body, SOAPAction)

#AlarmClock different putrequest!!

    def GetAlarms(self,Player):
        body = """<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:ListAlarms xmlns:u="urn:schemas-upnp-org:service:AlarmClock:1" />
            </s:Body>
            </s:Envelope>"""
        blen = len(body.encode())
        requestor = http.client.HTTPConnection(Player, self.SERVER_PORT)
        requestor.putrequest("POST", "/AlarmClock/Control HTTP/1.1")
        requestor.putheader("Host", Player)
        requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
        requestor.putheader("Content-Length", str(blen))
        requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:AlarmClock:1#ListAlarms")
        requestor.endheaders()
        requestor.send(body.encode())
        status = requestor.getresponse()
        ReturnV =[]
        try:
            reply_body = status.read()
            Alarm = 0
            Alarms = []
            while reply_body.find ('StartTime',Alarm+1) >0:
                Alarms.append (reply_body.find ('StartTime',Alarm+1))
                Alarm = reply_body.find ('StartTime',Alarm+1)
            for i in Alarms:
                Enabled = reply_body.find ('Enabled',i)
                Wert = reply_body [Enabled+14:Enabled+15]
                if Wert == '1':
                    RecEND = reply_body.find('&',i+78)
                    ReturnV.append (reply_body [i+78:RecEND])#Uhrzeit
                    ReturnV.append (reply_body [i+16:i+24]) #Wochentage
            return ReturnV
        except socket.error:
            return ReturnV

    def sonos_write_szene(self, player):
        dicti = {}
        dicti['MasterZone'] = "Own"
        posinfo = self.GetPositionInfo(player)
        pos = self.GetPosition(player)
        transinfo = self.GetTransportInfo(player)
        for zone in self.Zones:
            if zone in posinfo:
                dicti['MasterZone'] = zone
        if dicti.get('MasterZone') == "Own":
            if "PLAYING" in transinfo:
                dicti['Pause'] = 0
            else:
                dicti['Pause'] = 1
            if "file" in posinfo:
                dicti['Radio'] = 0
            else:
                dicti['Radio'] = 1
            antwort = posinfo
            pos1 = antwort.find ('<TrackURI>',0) #('*&quot;&gt;',0)
            pos2 = antwort.find ('</TrackURI>',0) #('&lt;/res&gt;&lt;r:',0)
            dicti['Sender'] = antwort [pos1+10:pos2]
            dicti['TitelNr'] = int(pos[0])
            dicti['Time'] = pos[1]
        dicti['Volume'] = self.GetVolume(player)
        if player == self.WohnZi:
            playern = "WohnZi"
            plnum = 33
        elif player == self.Kueche:
            playern = "Kueche"
            plnum = 40
        elif player == self.Bad:
            playern = "Bad"
            plnum = 34
        elif player == self.SchlafZi:
            playern = "SchlafZi"
            plnum = 35
        else:
            playern = player
            plnum = 0
        self.SaveList(player, playern, plnum)
        mysql_connector.mdb_set_table(table.name,self.Names.get(player),dicti)
        return True

    def soco_get_status(self, player, store = True, sznName=None, mainInfo=False):
        dicti = {}
        track_info = player.get_current_track_info()
        transinfo = player.get_current_transport_info()
        own_zone = player.uid
        zone = own_zone
        if False:
            zone = player.group.uid.split(':')[0]
        else:
            player_ip = player.ip_address
            posinfo = self.GetPositionInfo(player_ip)
            zones = self.get_zones()
            for _zone in zones:
                if _zone in posinfo:
                    zone = _zone
        name = player.player_name
        sznName = sznName or name
#        if player.is_coordinator:
        if zone == own_zone:
            dicti['MasterZone'] = ''
            dicti['Queue'] = player.get_queue()
            self.PLAYLISTS[name] = player.get_queue()
        else:
            dicti['MasterZone'] = zone
        dicti['Radio'] = not 'file' in track_info['uri']
        dicti['Sender'] = track_info['uri']
        dicti['TitelNr'] = track_info['playlist_position']
        dicti['Time'] = track_info['position']
        dicti['Name'] = name
        if not mainInfo:
            dicti['Volume'] = player.volume
            dicti['Pause'] = not transinfo['current_transport_state'] == 'PLAYING'        
        if store: self.Status[name] = dicti
        mysql_connector.mdb_set_table(table.name,sznName,dicti)  
        sonospl = player.get_sonos_playlist_by_attr('Title',name)
        player.remove_sonos_playlist(sonospl)
        player.create_sonos_playlist_from_queue(name)
        return dicti

    def soco_set_status(self,player):
        dicti = self.Status[player.player_name]
        tries = 0
        while (dicti != self.soco_get_status(player, store=False)) and tries < 7:
            tries += 1
            try:
                player_ip = player.ip_address
                self.SetVolume(player_ip, dicti.get('Volume'))
                if dicti['MasterZone'] != '':
                    master = self.get_player(dicti['MasterZone'])
                    player.join(master)
        #            self.CombineZones(player_ip, dicti['MasterZone'])
                else:
                    self.ClearZones(player_ip)
                    player.unjoin()
                    player.clear_queue()
                    for track in dicti['Queue']:
                        player.add_to_queue(track)
                    if dicti['Radio']:
                        self.setRadio(player_ip, dicti['Sender'])
                    else:
                        self.Seek(player_ip, "TRACK_NR", str(dicti['TitelNr']))
                        if str(dicti['Time']) != 'None':
                            self.Seek(player_ip, "REL_TIME", dicti['Time'])
                    if not dicti['Pause']:
                        player.play()
            except:
                time.sleep(tries)
                pass


    def soco_read_szene(self, player, sonos_szene, overrde_play=False):
        if str(sonos_szene.get('Volume')) != 'None':
            player.volume = sonos_szene.get('Volume')
        zone = sonos_szene.get('MasterZone')
        if (str(zone) != "None") and (str(zone) != "Own"):
            zonemaster, _, _, _ = self.get_addr(str(zone))
            player.join(zonemaster.group.coordinator)
        else:
            if str(zone) != "None":
                player.unjoin()
                player.clear_queue()
                if str(sonos_szene.get('Radio')) == '1':
                    player.play_uri(uri=str(sonos_szene.get('Sender')), start=False, force_radio=True)  
                else:
                    if isinstance(sonos_szene.get('PlayListNr'), int):
                        playlistItem = player.get_sonos_playlist_by_attr('item_id', 'SQ:'+ str(sonos_szene.get('PlayListNr')))
                        player.add_to_queue(playlistItem)
                    elif str(sonos_szene.get('PlayListNr')) != 'None':
                        playlistItem = player.get_sonos_playlist_by_attr('title', str(sonos_szene.get('PlayListNr')))
                        player.add_to_queue(playlistItem)
                    player.play_from_queue(sonos_szene.get('TitelNr'), start=False)
                    if str(sonos_szene.get('Time')) != 'None':
                        player.seek(sonos_szene.get('Time'))
            if (sonos_szene.get('Pause') == 1) or overrde_play:
                player.group.coordinator.pause()
            elif sonos_szene.get('Pause') == 0:
                player.group.coordinator.play()
        return True        

    def sonos_read_szene(self, player, sonos_szene, hergestellt = False):
        #read szene from Sonos DB and execute
        socoplayer = soco.SoCo(player)
        if str(sonos_szene.get('Volume')) != 'None':
            self.SetVolume(player, sonos_szene.get('Volume'))
        zone = sonos_szene.get('MasterZone')
        if (str(zone) != "None") and (str(zone) != "Own"):
            if 'RINCON' in str(zone):
                self.CombineZones(player, zone)
            else:
                _, z_ip, _, _ = self.get_addr(str(zone))
                to_att = soco.SoCo(z_ip)
                socoplayer.join(to_att.group.coordinator)
        else:
            zoneown = socoplayer.uid #self.sonos_zonen.get(str(player))
            if str(sonos_szene.get('Radio')) == '1':
                self.setRadio(player, str(sonos_szene.get('Sender')))
            elif str(zone) != "None":
                self.ClearZones(player)
                self.ClearList(player)
                if isinstance(sonos_szene.get('PlayListNr'), int):
                    self.PlayListNr(player, str(sonos_szene.get('PlayListNr')))
                elif str(sonos_szene.get('PlayListNr')) != 'None':
                    playlistItem = socoplayer.get_sonos_playlist_by_attr('title', str(sonos_szene.get('PlayListNr')))
                    socoplayer.add_to_queue(playlistItem)
#                    self.PlayListNr(player, str())
#                    playlist via soco
                self.ActivateList(player, zoneown)
                self.Seek(player, "TRACK_NR", str(sonos_szene.get('TitelNr')))
                if str(sonos_szene.get('Time')) != 'None':
                    self.Seek(player, "REL_TIME", sonos_szene.get('Time'))
            if (sonos_szene.get('Pause') == 1) or hergestellt:
                self.SetPause(player)
            elif sonos_szene.get('Pause') == 0:
                self.SetPlay(player)
        return True

    def durchsage(self,text):
        success = False
        players = list(soco.discover())
        while not success:
            try:
                self.Status = {}
                # save all zones
                for player in players:
                    t = threading.Thread(target=self.soco_get_status, args = [player])
                    t.start()
                mustend = time.time() + 5
                while (len(self.Status) < len(players)) and (time.time() < mustend):
                    time.sleep(0.25)
                success = True
            except:
                pass
        # combine all zones
        success = False
        while not success:
            try:
                for player in players:
                    if 'S1' in player.get_speaker_info()[u'model_number']:
                        self.SetVolume(player.ip_address, 10)
                    elif 'ZP90' in player.get_speaker_info()[u'model_number']:
                        self.SetVolume(player.ip_address, 65)
                    elif 'ZP120' in player.get_speaker_info()[u'model_number']:
                        self.SetVolume(player.ip_address, 40)
                soco.SoCo('192.168.192.203').partymode()
                mustend = time.time() + 5
                while (not len(soco.SoCo('192.168.192.203').all_groups) == 2) and (time.time() < mustend):
                    time.sleep(0.25)

        #        time.sleep(2)
                # source to PC
                soco.SoCo('192.168.192.203').switch_to_line_in()
                mustend = time.time() + 5
                while (not soco.SoCo('192.168.192.203').is_playing_line_in) and (time.time() < mustend):
                    time.sleep(0.25)

                soco.SoCo('192.168.192.203').play()
                mustend = time.time() + 5
                while (not soco.SoCo('192.168.192.203').get_current_transport_info()['current_transport_state'] == 'PLAYING') and (time.time() < mustend):
                    time.sleep(0.25)
                success = True
            except:
                pass
        # play file or text on PC
        play_wav(text)
        # resume all playback
        for player in players:
            player.unjoin()
            self.soco_set_status(player)
        return True

    def ansage(self,text,player_ip):
        player = soco.SoCo(player_ip)
        _, _, uid, _ = self.get_addr('Vm1ZIM1RUM1AV11')
        # save zone
        self.soco_get_status(player)
        # source to PC
        self.StreamInput(player_ip,uid)
        # play file or text on PC
        play_wav(text)
        # resume all playback
        self.soco_set_status(player)
        return True

    def isolate(self,player_ip):
        player = soco.SoCo(player_ip)
        if len(player.group.members) != 1:
            for device in player.group.members:
                device.unjoin()
        return True


    def play_local_file(self, player_n, text):
        """Add a non-py file from folder ./media and subfolders to soco"""
        # Make a list of music files, right now it is done by collection all files
        # below the current folder whose extension does not start with .py
        # This will probably need to be modded for other pusposes.
        location = constants.installation_folder + '/media/'
        if ('.wav' in text) or ('.mp3' in text):
            filename = text
        else:
            subprocess.call(["espeak", "-w " + location + "texttosonos.wav", "-a140", "-vmb-de6", "-p40", "-g0", "-s110", text])
            filename = "texttosonos.wav"
        # urlencode all the path parts (but not the /'s)
        random_file = os.path.join(
            *[quote(part) for part in os.path.split(filename)]
        )
        netpath = 'http://{}:{}/{}'.format(constants.eigene_IP, constants.sound_prov.PORT, random_file)
        for zone in soco.discover():
            if zone.player_name == player_n:
                break
        zoneown = zone.uid
        player_ip = zone.ip_address
        self.soco_get_status(zone)
        time.sleep(5)
        zone.unjoin()
        self.ActivateList(player_ip, zoneown)
        zone.clear_queue()
        zone.add_uri_to_queue(netpath)
        time.sleep(.1)
        zone.play()
        with contextlib.closing(wave.open(location+random_file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        time.sleep(duration)
        self.soco_set_status(zone)

    def set_device(self, player, command, text=''):
        # TODO: clean up this section
#        print(player, command)
#        if True:
        try:
            player, player_ip, p_uid, playerName = self.get_addr(player)
            if player in self.Devices:
                player = self.Devices.get(str(player))
                player, player_ip, p_uid, playerName = self.get_addr(player)
            # playerName = self.Names.get(player)
            if str(command) == "Pause":
                player.group.coordinator.pause()
            elif str(command) == "Play":
                player.group.coordinator.play()
            elif str(command) == "Save":
                player.soco_get_status()
            elif str(command) == "Announce_Time":
                player.soco_get_status()
                lt = localtime()
                stunde = int(strftime("%H", lt))
                minute = int(strftime("%M", lt))
                if (minute != 0) and (minute != 30):
                    text = "Es ist " + str(stunde) + " Uhr und " + str(minute) + " Minuten."
                    laenge = downloadAudioFile(text)
                    self.soco_read_szene(player, mysql_connector.mdb_read_table_entry(table.name,"TextToSonos"))
                    time.sleep(laenge + 1)
                    self.soco_read_szene(player, mysql_connector.mdb_read_table_entry(table.name,playerName))
            elif str(command) == "Durchsage":
                self.durchsage(text)
            elif str(command) == "Ansage":
                self.play_local_file(playerName, text)
            elif str(command) == "Return":
                self.soco_read_szene(player, mysql_connector.mdb_read_table_entry(table.name,playerName), overrde_play=True)
            elif ((str(command) == "resume") ):
                time.sleep(60)
                self.soco_read_szene(player, mysql_connector.mdb_read_table_entry(table.name,playerName))
            elif (str(command) == "lauter"):
                ActVol = player.volume
                increment = 8
                VOLUME = ActVol + increment
                player.volume = VOLUME
                return
            elif (str(command) == "leiser"):
                ActVol = player.volume
                increment = 8
                VOLUME = ActVol - increment
                player.volume = VOLUME
                return
            elif (str(command) == "inc_lauter"):
                ActVol = player.volume
                if ActVol >= 20: increment = 8
                if ActVol < 20: increment = 4
                if ActVol < 8: increment = 2
                VOLUME = ActVol + increment
                player.volume = VOLUME
            elif (str(command) == "inc_leiser"):
                ActVol = player.volume
                if ActVol >= 20: increment = 8
                if ActVol < 20: increment = 4
                if ActVol < 8: increment = 2
                VOLUME = ActVol - increment
                player.volume = VOLUME
            elif (str(command) == "WeckerAnsage"):
                self.SetPause(player_ip)
                self.SetVolume(player_ip, 20)
                mysql_connector.setting_s("Durchsage", str(crn.next_wecker_heute_morgen()))
                text = mysql_connector.setting_r("Durchsage")
                laenge = downloadAudioFile(text)
                self.soco_read_szene(player, mysql_connector.mdb_read_table_entry(table.name,"TextToSonos"))
                time.sleep(laenge + 1)
                self.SetPause(player_ip)
            elif (str(command) == "EingangWohnzi"):
                self.StreamInput(player_ip, self.WohnZiZone)
            elif (str(command) == "SpeicherFavorit"):
                self.soco_get_status(player, sznName='Favorit', mainInfo=True)                
            elif (str(command) == "Isolieren"):
                self.isolate(player_ip)
            elif ((str(command) != "resume") and (str(command) != "An") and (str(command) != "None")):
                sonos_szene = mysql_connector.mdb_read_table_entry(table.name,command)
                self.soco_read_szene(player, sonos_szene)
            return True
        except:
            return False

    def list_commands(self):
        comands = mysql_connector.mdb_get_table(table.name)
        liste = ["Pause","Play","Save","Announce_Time","Durchsage",'Ansage',"Return","resume","lauter",
                 "leiser","inc_leiser","inc_lauter","WeckerAnsage", "EingangWohnzi","Isolieren","SpeicherFavorit"]
        for comand in comands:
            liste.append(comand.get("Name"))
        #liste.remove("Name")
        return liste

    def dict_commands(self):
        #comands = mdb_get_table(table.name)
        dicti = {}
        dicti[''] = 1
        liste = sorted(self.list_commands())
        for key, item in enumerate(liste):
            dicti[str(item)] = key + 2
        return dicti

    def list_devices(self):
        return [player.player_name for player in self.socoDiscover()]
#        comands = mysql_connector.mdb_read_table_entry(constants.sql_tables.szenen.name,"Device_Type")
#        liste = []
#        for comand in comands:
#            if comands.get(comand) == "SONOS":
#                liste.append(comand)
#        #liste.remove("Name")
#        return liste

