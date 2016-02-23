# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:43:14 2016

@author: christoph
"""

import constants

from mysql_con import inputs

import socket

PORT_NUMBER = constants.udp_.PORT
mySocket = socket.socket()# socket.AF_INET, socket.SOCK_STREAM )
mySocket.bind( ('', PORT_NUMBER) )
mySocket.listen(5)
SIZE = 1024

def main():
    while constants.run:
        conn, addr = mySocket.accept()
        data = conn.recv(1024)
        print data
        if not data:
            break
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
        except Exception as serr:
            isdict = False 
        conn.send(data)
        conn.close()  
        if isdict:
            if ('Name' in data_ev) and ('Value' in data_ev):
                print data_ev
                #szns = inputs(data_ev.get('Name'),data_ev.get('Value'))

if __name__ == '__main__':
    main()    
