#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 18:11:12 2021

@author: christoph
"""

from kodipydent import Kodi
import constants
import time
from tools import toolbox


class kodi_client():
    def __init__(self):
        success = False
        while not success:
            try:
                self.my_kodi = Kodi('192.168.192.171')
                success = True
                print('Kodi connected')
            except Exception as e:
                pass 
        toolbox.communication.register_callback(self.callback_receiver)    
        

    def slideshow(self):
        try:
            self.my_kodi.Player.Open(item={"directory":"/storage/pictures/"})
        except Exception as e:
            pass
        
    def stop(self):
        try:
            players = self.my_kodi.Player.GetActivePlayers()['result']
            for player in players:
                self.my_kodi.Player.Stop(player)
        except Exception as e:
            pass
        
    def show_noti(self, text):
        try:
            self.my_kodi.GUI.ShowNotification(title='Haus', message=text)
        except Exception as e:
            pass
        
    
    def callback_receiver(self, payload, *args, **kwargs):
        if toolbox.kw_unpack(kwargs,'typ') == 'Setting':
            if payload['Setting'] == 'Status':
                if payload['Value'] == 'Wach':
                    self.slideshow()
                else:
                    self.stop()


def main():
    kodi = kodi_client()
    while constants.run:
        time.sleep(100)
        
if __name__ == "__main__":
    main()
        
        
    