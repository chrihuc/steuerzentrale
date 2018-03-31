# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:43:14 2016

@author: christoph
"""

import threading
import socket
import struct
import time
import sys
import json
import datetime

import constants

from database import mysql_connector as msqc
from alarm_event_messaging import alarmevents as aevs
from alarm_event_messaging import messaging
from outputs import szenen
from outputs import cron

from tools import toolbox
#toolbox.log('debug on')

# TODO: unittest?

hostName = socket.gethostbyname( constants.eigene_IP )

biSocket = socket.socket()# socket.AF_INET, socket.SOCK_STREAM )
biSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
biSocket.bind( (hostName, constants.udp_.biPORT) )
biSocket.listen(10)

biSocket_n = socket.socket()# socket.AF_INET, socket.SOCK_STREAM )
biSocket_n.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
biSocket_n.bind( (hostName, 5050) )
biSocket_n.listen(10)

PORT_NUMBER = constants.udp_.PORT
broadSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadSocket.bind( (hostName, constants.udp_.broadPORT) )

borad_to_guis = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
borad_to_guis.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

scenes = szenen.Szenen()
aes = aevs.AES()
mes = messaging.Messaging()
crn = cron.Cron()

SIZE = 4096

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.seconds
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def exec_data(data_ev, data):
    if ('Name' in data_ev) and ('Value' in data_ev):
        name = data_ev.get('Name')
        value = data_ev.get('Value')
        szenen.Szenen.trigger_scenes(name, value)
#        szns, desc = msqc.inputs(name,value)
#        for szene in szns:
#            if szene <> None:
#                scenes.threadExecute(szene, check_bedingung=False, wert=value, device=desc)
#    elif data_ev.get('Command')=='Update':
#        aes.new_event(description="System update", prio=0)
#        cmd_internal.git_update()
    elif ('Szene' in data_ev):
        name = data_ev.get('Szene')
        if name in msqc.mdb_read_table_column(constants.sql_tables.szenen.name, 'Name'):
            scenes.threadExecute(name)
    elif ('Android_id' in data_ev):
        # aes.new_event('Register new Client: ' + data_ev.get('Name'))
        mes.register_user(data_ev)
    elif ('Device' in data_ev) and ('Command' in data_ev):
        scenes.threadSetDevice(data_ev['Device'], data_ev['Command'])
    elif ('Request_js' in data_ev):
        toolbox.log(data_ev)
        if data_ev.get('Request_js') == 'Wecker':
            data = json.dumps(crn.get_all(wecker=True), default=handler)
        elif data_ev.get('Request_js') == 'Settings':
            data = json.dumps(msqc.settings_r(), default=handler)
        elif data_ev.get('Request_js') == 'Inputs_hks':
            msqc.tables.reload_inputs()
            data = json.dumps(msqc.tables.inputs_dict_hks, default=handler, allow_nan=False)
    elif ('Request' in data_ev):
        if data_ev.get('Request') == 'Settings':
            data = str(msqc.settings_r())
        elif data_ev.get('Request') == 'Inputs':
            data = str(msqc.inputs_r())
        elif data_ev.get('Request') == 'Bewohner':
            data = str(msqc.mdb_get_table(constants.sql_tables.Bewohner.name))
        elif data_ev.get('Request') == 'Besucher':
            data = str(msqc.mdb_get_table(constants.sql_tables.Besucher.name))
        elif data_ev.get('Request') == 'Wecker':
            data = crn.get_all(wecker=True)
        elif data_ev.get('Request') == 'GuiAlarms':
            data = crn.get_all(typ='Gui')
    elif ('SetWecker' in data_ev):
        table = constants.sql_tables.cron.name
        for entry in eval(data_ev['SetWecker']):
            device = entry['Name']
            msqc.mdb_set_table(table, device, entry)
    elif ('Log' in data_ev):
        borad_to_guis.sendto(str(data_ev),('192.168.192.255',5000))
    return data


# todo fix!!!!!!!!!!!!
def bidirekt():
    while constants.run:
        conn, addr = biSocket.accept()
        try:
            data = conn.recv(SIZE)
            toolbox.log(data)
            if not data:
                conn.close()
                break
            isdict = False
            try:
                data_ev = eval(data)
                if type(data_ev) is dict:
                    isdict = True
            except Exception as serr:
                try:
                    data_ev = eval(data[2:])
                    if type(data_ev) is dict:
                        isdict = True
                except Exception as serr:
                    isdict = False
            if isdict:
                data = exec_data(data_ev, data)

            #conn.sendall(data)
            conn.send(data)
#            send_msg(conn)
        finally:
            conn.close()

def bidirekt_new():
    while constants.run:
        conn, addr = biSocket_n.accept()
        try:
            data = recv_msg(conn)
            print data
            toolbox.log(data)
            if not data:
                conn.close()
                break
            isdict = False
            try:
                data_ev = eval(data)
                if type(data_ev) is dict:
                    isdict = True
            except Exception as serr:
                try:
                    data_ev = eval(data[2:])
                    if type(data_ev) is dict:
                        isdict = True
                except Exception as serr:
                    isdict = False
            if isdict:
                data = exec_data(data_ev, data)

            send_msg(conn, data)
        finally:
            conn.close()

def broadcast():
    while constants.run:
        (data,addr) = broadSocket.recvfrom(SIZE)
        toolbox.log(data)
        if not data:
            break
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
        except Exception as serr:
            isdict = False
        if isdict:
            exec_data(data_ev, data)

def main():
    constants.run = True
    threadliste = []

    t = threading.Thread(name="bidirekt", target=bidirekt, args = [])
    threadliste.append(t)
    t.start()

    t = threading.Thread(name="broadcast", target=broadcast, args = [])
    threadliste.append(t)
    t.start()

    try:
        while constants.run:
            for t in threadliste:
                if not t in threading.enumerate():
                    toolbox.log(t.name)
                    constants.run = False
                    sys.exit()
            time.sleep(10)
    except KeyboardInterrupt:
        constants.run = False
        sys.exit()

if __name__ == '__main__':
    main()
