import httplib
import requests
import time
from time import localtime,strftime
from datetime import date

#AVTransport (GetTransportInfo, SetPause, SetPlay, CombineZones, StreamInput, ClearZones, AddTrack, RemoveTrack, GetPosition, GetPositionInfo, Seek, ActivateList, ClearList, PlayList (defect), PlayListNr)
#RenderingControl (SetMute, GetVolume, SetVolume)

#Envelope for all AVTrans actions the same
def Envelope(self, Player, body, SOAPAction):  
    blen = len(body)
    requestor = httplib.HTTP(Player, self.SERVER_PORT)
    requestor.putrequest("POST", "/MediaRenderer/AVTransport/Control HTTP/1.1")
    requestor.putheader("HOST", Player)
    requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
    requestor.putheader("Content-Length", str(blen))
    requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:" + SOAPAction)
    requestor.endheaders()
    requestor.send(body)
    (status_code, message, reply_headers) = requestor.getreply()
    reply_body = requestor.getfile().read()  
    return reply_body

#Envelope for all RendCont actions the same
def EnvelopeRC(self, Player, body, SOAPAction):
    blen = len(body)
    requestor = httplib.HTTP(Player, self.SERVER_PORT)
    requestor.putrequest("POST", "/MediaRenderer/RenderingControl/Control HTTP/1.1")
    requestor.putheader("Host", Player)
    requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
    requestor.putheader("Content-Length", str(blen))
    requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:" + SOAPAction)
    requestor.endheaders()
    requestor.send(body)
    (status_code, message, reply_headers) = requestor.getreply()
    reply_body = requestor.getfile().read()
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

def main():
    sn = sonos()
    #sn.ClearZones(sn.Bad)
    print sn.SaveList(sn.Bad, "Bad", "34")
    print sn.Names.get(sn.Bad)
    #sn.ActivateList(sn.Bad, sn.BadZone)
    #sn.SetPlay(sn.Bad)

class sonos:
    def __init__(self):
        self.WohnZi = "192.168.192.201"
        self.SchlafZi = "192.168.192.202"
        self.Bad = "192.168.192.203"
        self.Kueche = "192.168.192.204"        
        self.SchlafZiZone = "RINCON_000E5830220001400"
        self.BadZone = "RINCON_000E583138BA01400"
        self.WohnZiZone = "RINCON_000E58232A2601400"
        self.KuecheZone = "RINCON_000E58CB9E3E01400"  
        self.Zones = [self.SchlafZiZone, self.BadZone, self.WohnZiZone, self.KuecheZone]
        self.Names = {self.SchlafZi:"SchlafZi", self.Bad:"Bad", self.WohnZi:"WohnZi", self.Kueche:"Kueche"}
        self.SERVER_PORT = 1400
        self.VOLUME = 0

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
        Envelope(self, Player, body, SOAPAction)

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
                <Target>""" + Position + """</Target>
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
        blen = len(body)
        requestor = httplib.HTTP(Player, self.SERVER_PORT)
        requestor.putrequest("POST", "/AlarmClock/Control HTTP/1.1")
        requestor.putheader("Host", Player)
        requestor.putheader("Content-Type", """text/xml; charset="utf-8" """)
        requestor.putheader("Content-Length", str(blen))
        requestor.putheader("SOAPAction", "urn:schemas-upnp-org:service:AlarmClock:1#ListAlarms")
        requestor.endheaders()
        requestor.send(body)
        (status_code, message, reply_headers) = requestor.getreply()
        ReturnV =[]
        try:
            reply_body = requestor.getfile().read()
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

if __name__ == '__main__':
    main()
