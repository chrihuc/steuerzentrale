#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:06:57 2017

@author: christoph
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 09 12:14:56 2017

@author: 212505558
"""

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.cache import Cache

import socket
import subprocess as sp
import datetime
import constants
import threading

from kivy.properties import ObjectProperty, StringProperty, OptionProperty, \
    ListProperty, NumericProperty, AliasProperty, BooleanProperty


running = True

def get_data(requ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_ev = {'Request':str(requ)}
    s.connect(('192.168.192.10',5005))
    s.send(str(data_ev))
    reply = s.recv(2048)
    return eval(reply)
    
    
class AlarmClock(ScrollView):
    
    def __init__(self, **kwargs):
        super(AlarmClock, self).__init__(**kwargs)   
        self.size_hint=(1, 1)
        # cols, TimePicker, Mo, Di, Mi, Do, Fr, Sa, So, Sz, Enabled
        layout = GridLayout(cols=1, spacing=10, size_hint=(None,None))
        # set size of layout
        layout.bind(minimum_height=layout.setter('height'), minimum_width=layout.setter('width'))
        # 20 alarms
        for cnt in range(20):
            # Make sure the height is such that there is something to scroll.
            row = GridLayout(rows=1, spacing=5, size_hint=(None,None))
            row.bind(minimum_height=row.setter('height'), minimum_width=row.setter('width'))
            spinner = Spinner(text='30', values=(str(num) for num in range(24)),
                              size_hint=(None, None), size=(40, 40)) 
            row.add_widget(spinner)
            spinner = Spinner(text='30', values=(str(num) for num in range(60)),
                              size_hint=(None, None), size=(40, 40)) 
            row.add_widget(spinner) 
            spacer = Widget(size_hint=(None, None), size=(20, 40))
            row.add_widget(spacer)
            for i in range(2,15):
                btn = ToggleButton(text=str(i), size_hint=(None,None), size=(80,40), state='down')
                row.add_widget(btn)
            layout.add_widget(row)
        self.add_widget(layout)  

class PictureFrame(ModalView):
    
    def __init__(self, **kwargs):
        super(PictureFrame, self).__init__(**kwargs)
        self.bind(on_touch_down=self.dismiss)

class ScreenSaver_handler(object):
    def __init__(self, go_home):
        self.last_event = datetime.datetime.now()
        Window.bind(on_motion=self.on_motion)
        Clock.schedule_interval(self.slideshow, .5)
        self.ss_on = False
        self.pic_frame = PictureFrame()
        self.go_home = go_home
        
    def slideshow(self, *args):
        if datetime.datetime.now() - self.last_event > datetime.timedelta(hours=0, minutes=0, seconds=5):
            if not self.ss_on:
                self.pic_frame.open()
                self.ss_on = True
                self.go_home()
    
    def on_motion(self, *args, **kwargs):
        self.last_event = datetime.datetime.now()
        self.pic_frame.dismiss()
        self.ss_on = False   


class OpScreen(TabbedPanel):

    def __init__(self, **kwargs):
        super(OpScreen, self).__init__(**kwargs) 
        self.screnns = ScreenSaver_handler(self.go_home)
        self.aimg = AsyncImage(source='http://192.168.192.36/html/cam.jpg', nocache = True, size_hint=(1, 1))
        self.populate_szenen()
        self.populate_wecker()
        self.populate_webcam()
        self.update_labels()
        Clock.schedule_interval(self.populate_settings, 60)
        threading.Thread(target=self.udp_thread).start()
    
    def go_home(self):
        self.switch_to(self.ids.EG)

    def klingel(self):
        self.screnns.on_motion()
        self.switch_to(self.ids.Kamera)
        self.update_webcam()

    def populate_settings(self):
        for widg in self.ids:
            if hasattr(constants.gui_, widg):
                value = getattr(constants.gui_, widg)
                if isinstance(value, (bool)):
                    if value:
                        print widg, value
                        self.ids[widg].state = 'down'   

    def change_setting(self, _id):
        if isinstance(self.ids[_id], ToggleButton):
            if self.ids[_id].state == 'down':
                value = True
            else:
                value = False
        setattr(constants.gui_, _id, value)
        constants.save_config()

    def populate_szenen(self):
        for tab in self.tab_list:
            if tab.text == 'Szenen':
                splitter = GridLayout(cols=2, spacing=10, size_hint_y=None)
                layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
                layout2 = GridLayout(cols=1, spacing=10, size_hint_y=None)
                # Make sure the height is such that there is something to scroll.
                layout.bind(minimum_height=layout.setter('height'))
                for i in range(100):
                    btn = Button(text=str(i), size_hint_y=None, height=40)
                    btn.bind(on_press=lambda x, i=i: self.print_text(i))
                    layout.add_widget(btn)
                sview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                sview.add_widget(layout)   
                splitter.add_widget(sview) 
                sview2 = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                sview2.add_widget(layout2)
                splitter.add_widget(sview2)                
                tab.add_widget(splitter)

    def populate_webcam(self, *args, **kwargs):
        self.ids.KamBox.add_widget(self.aimg)

    def update_labels(self):
        settings = get_data('Settings')
        for widg in self.ids:
            if widg in settings:
                if widg[11:13] == 'TE':
                    self.ids[widg].text = '[ref='+widg+']'+settings[widg]+' degC[/ref]'

    def update_webcam(self, *args, **kwargs):
        self.aimg.reload()
#        for tab in self.tab_list:
#            if tab.text == 'Kamera':
#                print tab.children
#                for child in tab.children:
#                    tab.remove_widget(child)
    
    def show_ontouchevent(self, *args, **kwargs):
        for item in args:
            print item
        for key, value in kwargs.iteritems():
            print key, value
        
    def populate_wecker(self):
        for tab in self.tab_list:
            if tab.text == 'Wecker':
                alarme = AlarmClock()
                tab.add_widget(alarme)                
        
    def populate_wecker_old(self):
        for tab in self.tab_list:
            if tab.text == 'Wecker':
                vert_scroll_layout = GridLayout(cols=1, spacing=40, size_hint_y=None)
                vert_scroll_layout.bind(minimum_height=vert_scroll_layout.setter('height'))
                vert_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                vert_scroll_view.add_widget(vert_scroll_layout)
                
                # add wecker row
                for cnt in range(20):
                    hor_scroll_layout = GridLayout(rows=1, spacing=10, size_hint_x=None)
                    hor_scroll_layout.bind(minimum_width=hor_scroll_layout.setter('width'))
                    hor_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 40))
                    hor_scroll_view.add_widget(hor_scroll_layout)
                    
                    for j in range(20):
                        btn = Button(text=str(j), size_hint_x=None, width=40)
#                        btn.bind(on_press=lambda x, i=i: self.print_text(i))
                        hor_scroll_layout.add_widget(btn) 
                    vert_scroll_layout.add_widget(hor_scroll_view)
                    
                tab.add_widget(vert_scroll_view)

    def udp_thread(self, *args):
        broadSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        hostName = socket.gethostbyname( '192.168.192.255')#constants.eigene_IP )
        broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadSocket.bind( (hostName, constants.udp_.broadPORT))
        SIZE = 1024
        while running:
            try:
                (data,addr) = broadSocket.recvfrom(SIZE)
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
                if isdict:
                    if data_ev['Name'] == 'Klingel':
                        self.klingel()
                    elif data_ev['Name'] == 'DisplayAn':
                        pass
                    elif data_ev['Name'] == 'DisplayAus':
                        pass                       
            except socket.error, e:
                if e.errno != 4:
                    raise 

    def print_text(self, text):
        print text

class TemperaturLabel(Label):
    def pop_up(self, *args):
        popup = Popup(title='Test popup',
            content=Label(text='Hello world'),
            size_hint=(None, None), size=(400, 400))   
        popup.open()

class LichtButton(Button):
    def pop_up(self, *args):
        popup = Popup(title='Test popup',
            content=Label(text='Hello world'),
            size_hint=(None, None), size=(400, 400))   
        popup.open()

class GuiApp(App):
    def build(self):
        self.OpScreen = OpScreen()
#        self.OpScreen.after_build()
        return self.OpScreen
        
#    def on_start(self):
#        self.OpScreen.after_build()


if __name__ == '__main__':
    GuiApp().run()