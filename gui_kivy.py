#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:06:57 2017

@author: christoph
"""

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.config import Config

from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.cache import Cache

from kivy.uix.slider import Slider

from kivy.lang import Builder
from kivy.cache import Cache
from kivy.garden.graph import Graph, MeshLinePlot

import time
import io
import pygame as pg
from urllib2 import urlopen

import random
import os
import socket
import subprocess as sp
import datetime
import constants
import threading
import pandas as pd
import MySQLdb as mdb

from database import kivy_mysql_connector as kmc
#from outputs import sonos
#from outputs import xs1
#from outputs import hue
#from outputs import samsung
#from outputs import satellites
#from outputs import szenen
#from outputs import cron

from kivy.properties import ObjectProperty, StringProperty, OptionProperty, \
    ListProperty, NumericProperty, AliasProperty, BooleanProperty

#xs1 = xs1.XS1(constants.xs1_.IP)
#hue = hue.Hue_lights()
#sn = sonos.Sonos()
#tv = samsung.TV()
#sat = satellites.Satellite()
#scenes = szenen.Szenen()
#crons = cron.Cron()

pg.init()
running = True
con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
pd_szenen = pd.read_sql('SELECT * FROM set_Szenen', con=con)
con.close()

Config.set('kivy', 'log_level', 'debug')

def get_data(requ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    data_ev = {'Request':str(requ)}
    s.connect(('192.168.192.10',5005))
    s.send(str(data_ev))
    reply = s.recv(2048)
    s.close()
    return eval(reply)


class AssImage(AsyncImage):
    def __init__(self, **kwargs):
        super(AssImage, self).__init__(**kwargs)

    def reload(self,**kwargs):
        Cache.remove('kv.loader')
        super(AssImage, self).reload(**kwargs)


class AlarmClock(ScrollView):

    def __init__(self, typ, **kwargs):
        super(AlarmClock, self).__init__(**kwargs)
        self.size_hint=(1, 1)
        # cols, TimePicker, Mo, Di, Mi, Do, Fr, Sa, So, Sz, Enabled
        self.layout = GridLayout(cols=1, spacing=5, size_hint=(None,None))
        # set size of layout
        self.layout.bind(minimum_height=self.layout.setter('height'), minimum_width=self.layout.setter('width'))
        self.typ = typ
#        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
#        self.pd_alarme = pd.read_sql('SELECT * FROM cmd_cron', con=con)
#        con.close()
        self.set_load_button()

    def set_load_button(self):
        self.clear_widgets()
        self.layout.clear_widgets()
        btn = Button(text=str('Load'), size_hint=(None,None), size=(200,200))
        btn.bind(on_press=self.update)
        self.layout.add_widget(btn)
        self.add_widget(self.layout)
#        self.update()

    def update(self, *args):
        self.clear_widgets()
        self.layout.clear_widgets()
        con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
        self.pd_alarme = pd.read_sql('SELECT * FROM cmd_cron', con=con)
        con.close()
        reihen = self.pd_alarme.loc[self.pd_alarme['Type']==self.typ]
        for i, reihe in reihen.iterrows():
            # Make sure the height is such that there is something to scroll.
            row = GridLayout(rows=1, spacing=5, size_hint=(None,None))
            row.bind(minimum_height=row.setter('height'), minimum_width=row.setter('width'))
#            print row
            row.id = str(i)
            if self.typ == 'Wecker':
                szenenlist = kmc.list_scenes('Wecker')
            else:
                szenenlist = kmc.list_scenes(['Favorit', 'Gui'])
            spinner = Spinner(text=reihe['Szene'], values=szenenlist,
                              size_hint=(None, None), size=(140, 40))
            spinner.id = 'Szene'
            row.add_widget(spinner)
            if isinstance(reihe['Time'], datetime.timedelta):
                hour = reihe['Time'].seconds // 3600
                minutes = (reihe['Time'].seconds % 3600) / 60
            else:
                print reihe['Time']
                hour = ((reihe['Time']) /1000000000 )// 3600
                minutes = (((reihe['Time']) /1000000000 ) % 3600) / 60
            spinner = Spinner(text=str(hour), values=(str(num) for num in range(24)),
                              size_hint=(None, None), size=(40, 40))
            spinner.id = 'hour'
            row.add_widget(spinner)
            colon = Label(text=':')
            row.add_widget(colon)
            spinner = Spinner(text=str(minutes), values=(str(num) for num in range(60)),
                              size_hint=(None, None), size=(40, 40))
            spinner.id = 'min'
            row.add_widget(spinner)
            spacer = Widget(size_hint=(None, None), size=(20, 40))
            row.add_widget(spacer)
            for i in ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']:
                btn = ToggleButton(text=str(i), size_hint=(None,None), size=(80,40))
                btn.id = i
                if eval(reihe[i]):
                    btn.state='down'
                row.add_widget(btn)
            spacer = Widget(size_hint=(None, None), size=(20, 40))
            row.add_widget(spacer)
            btn = ToggleButton(text=str('An'), size_hint=(None,None), size=(80,40))
            if eval(reihe['Eingeschaltet']):
                btn.state='down'
            btn.id = 'Eingeschaltet'
            row.add_widget(btn)
            self.layout.add_widget(row)
        btn = Button(text=str('Save'), size_hint=(None,None), size=(80,40))
        btn.bind(on_press=self.save)
        self.layout.add_widget(btn)
        self.add_widget(self.layout)

    def save(self, *args):
        for kid in self.layout.children:
            time = 0
            for baby in kid.children:
                if baby.id == 'hour':
                    time += int(baby.text) * 60
                elif baby.id == 'min':
                    time += int(baby.text)
#                    self.pd_alarme[self.pd_alarme['Id']==int(kid.id)][baby.id] = baby.text
                elif baby.id in ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So', 'Eingeschaltet']:
#                    print kid.id, baby.id, baby.state == 'down'
                    pass
                    self.pd_alarme.set_value(int(kid.id), baby.id, baby.state == 'down')
#                    self.pd_alarme[self.pd_alarme['Id']==int(kid.id)][baby.id] = baby.state == 'down'
            print time
        print self.pd_alarme


class PictureFrame(ModalView):

    def __init__(self, **kwargs):
        super(PictureFrame, self).__init__(**kwargs)
        self.bind(on_touch_down=self.dismiss)
        self.base_dir = constants.gui_.Bilder
        imgs = [os.path.join(self.base_dir, img) for img in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, img))]
        self.carousel = Carousel(direction='right', loop=True)
        random.shuffle(imgs)
        for img in imgs:
            image = AsyncImage(source=img, nocache=True)
            self.carousel.add_widget(image)
        self.add_widget(self.carousel)

        self.delay = 5
        #self.load_next_p()
        self.clock_event = None

    def load_next_p(self, *args):
        imgs = [os.path.join(self.base_dir, img) for img in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, img))]
        random.shuffle(imgs)
        self.carousel.clear_widgets()
        try:
            image = AsyncImage(source=imgs[0], nocache=True)
            self.carousel.add_widget(image)
        except:
            pass
# TODO: stop clock
        self.clock_event = Clock.schedule_once(self.load_next, self.delay)

    def dismiss(self, *args,**kwargs):
        super(PictureFrame, self).dismiss()
        if self.clock_event != None:
            self.clock_event.cancel()

    def start_show(self):
        self.open()
        self.clock_event = Clock.schedule_interval(self.carousel.load_next, self.delay)

class ScreenSaver_handler(object):
    def __init__(self, go_home):
        self.last_event = datetime.datetime.now()
        Window.bind(on_motion=self.on_motion)
        Clock.schedule_interval(self.slideshow, .5)
        self.ss_on = False
        self.state_awake = False
        self.pic_frame = PictureFrame()
        self.go_home = go_home

    def slideshow(self, *args):
        if datetime.datetime.now() - self.last_event > datetime.timedelta(hours=0, minutes=0, seconds=20):
            if not self.ss_on:
                if constants.gui_.Feh and self.state_awake:
                    self.backlight(100)
                    self.pic_frame.start_show()
                else:
#                    exectext = 'sudo /bin/su -c "echo 0 > /sys/class/backlight/rpi_backlight/brightness"'
                    self.backlight(0)
                self.ss_on = True
                self.go_home()

    def on_motion(self, *args, **kwargs):
        self.last_event = datetime.datetime.now()
        self.pic_frame.dismiss()
        self.backlight(100)
        self.ss_on = False

    def backlight(self, value):
        if not constants.gui_.KS:
            return
        exectext = 'echo %s > /sys/class/backlight/rpi_backlight/brightness' % (value)
        os.system(exectext)

class OpScreen(TabbedPanel):

    def __init__(self, **kwargs):
        super(OpScreen, self).__init__(**kwargs)
        self.alarme = AlarmClock('Wecker')
        self.schaltuhr = AlarmClock('Gui')
        self.play_wc = False
        self.screnns = ScreenSaver_handler(self.go_home)
        self.im_url = 'http://192.168.192.36/html/cam.jpg'
        self.load_spy_pic()
        self.aimg = Image(source='spy.jpg')
#        self.aimg = AssImage(source='http://192.168.192.36/html/cam.jpg', size_hint=(1, 1))#, nocache = True)
        self.populate_szenen()
        self.populate_wecker()
        self.populate_webcam()
        self.populate_settings()
        self.update_labels()
        self.bind(current_tab=self.tab_change)

        self.some_label = Label()
        self.my_slider = Slider()
        self.my_slider.bind(value=self.OnSliderValueChange)

        if constants.gui_.KS:
            pass
#            Window.fullscreen = True
        Clock.schedule_interval(self.update_labels, 60)
        threading.Thread(target=self.udp_thread).start()

    def go_home(self):
        self.switch_to(self.ids.EG)

    def klingel(self):
        if constants.gui_.KlingelAn:
            self.screnns.on_motion()
        self.switch_to(self.ids.Kamera)
        self.update_webcam()

    def populate_settings(self, *args):
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
#        Window.fullscreen = constants.gui_.KS
        setattr(constants.gui_, _id, value)
        constants.save_config()


    def OnSliderValueChange(self, instance,value):
        self.some_label.text = str(value)


    def populate_szenen(self):
        favoriten = pd_szenen.loc[pd_szenen['Gruppe'] == 'Favorit']
        guis = pd_szenen.loc[pd_szenen['Gruppe'] == 'Lichter']
        for tab in self.tab_list:
            if tab.text == 'Szenen':
                splitter = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
                layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
                layout2 = GridLayout(cols=1, spacing=10, size_hint_y=None)
                # Make sure the height is such that there is something to scroll.
                layout.bind(minimum_height=layout.setter('height'))
#                splitter.bind(minimum_height=splitter.setter('height'))
                layout2.bind(minimum_height=layout2.setter('height'))
                for i, szene in favoriten.iterrows():
                    btn = Button(text=str(szene['Beschreibung']), size_hint_y=None, height=40)
                    commando = szene['Name']
                    btn.bind(on_press=lambda x, commando=commando: self.execute_szn(commando))
                    layout.add_widget(btn)
                for i, szene in guis.iterrows():
                    btn = Button(text=str(szene['Beschreibung']), size_hint_y=None, height=40)
                    commando = szene['Name']
                    btn.bind(on_press=lambda x, commando=commando: self.execute_szn(commando))
                    layout2.add_widget(btn)
                sview = ScrollView(size_hint=(1, 1))
                sview.add_widget(layout)
                splitter.add_widget(sview)
                sview2 = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                sview2.add_widget(layout2)
                splitter.add_widget(sview2)
                tab.add_widget(splitter)

    def execute_szn(self, szene):
        commado = {'Szene':szene}
        csocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        csocket.sendto(str(commado),(constants.udp_.SERVER,constants.udp_.broadPORT))
        csocket.close()

    def populate_webcam(self, *args, **kwargs):
        self.ids.KamBox.clear_widgets()
        self.ids.KamBox.add_widget(self.aimg)

    def update_labels(self, *args):
        try:
            settings = get_data('Settings')
            for widg in self.ids:
                if widg in settings:
                    if widg[11:13] == 'TE':
                        self.ids[widg].text = settings[widg]+' degC'
                    elif widg[11:13] == 'CO':
                        self.ids[widg].text = settings[widg]+' ppm'
        except socket.error:
            pass

    def load_spy_pic(self):
        image_str = urlopen(self.im_url).read()
        image_file = io.BytesIO(image_str)
        image = pg.image.load(image_file)
        pg.image.save(image, 'spy.jpg')        

    def update_webcam(self, *args, **kwargs):
#        self.populate_webcam()
        self.load_spy_pic()
        time.sleep(0.2)
        self.aimg.reload()
        if self.play_wc: Clock.schedule_once(self.update_webcam, 0.25)

    def play_webcam(self):
        self.play_wc = True

    def stop_webcam(self):
        self.play_wc = False

    def populate_wecker(self):
        for tab in self.tab_list:
            if tab.text == 'Wecker':
                tab.add_widget(self.alarme)
            if tab.text == 'Zeitschaltuhr':
                tab.add_widget(self.schaltuhr)

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
                    try:
                        if data_ev['Name'] == 'Klingel':
                            self.klingel()
                        elif data_ev['Name'] == 'DisplayAn':
                            self.screnns.state_awake = True
                            self.screnns.ss_on = False
                        elif data_ev['Name'] == 'DisplayAus':
                            self.screnns.state_awake = False
                            self.screnns.ss_on = False
                    except:
                        print data
            except socket.error, e:
                if e.errno != 4:
                    raise

    def tab_change(self, *args):
        if args[1].text == 'Wecker':
            self.alarme.set_load_button()
        elif args[1].text == 'Zeitschaltuhr':
            self.schaltuhr.set_load_button()

    def print_text(self, *args):
        for arg in args:
            print dir(arg)

    def licht_button_pop_up(self, device):
        dev_type = pd_szenen.get_value(0,device)
        desc = pd_szenen.get_value(4,device)
        self.popup = Popup(title=desc,
            size_hint=(None, None), size=(400, 400))
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
#        if dev_type == 'XS1':
#            for item in xs1.list_commands():
#                btn = Button(text=str(item), size_hint_y=None, height=40)
#                btn.bind(on_press=self.send_dev_command)
#                layout.add_widget(btn)
#        elif dev_type == 'HUE':
#            for item in hue.list_commands():
#                btn = Button(text=str(item), size_hint_y=None, height=40)
#                btn.bind(on_press=self.send_dev_command)
#                layout.add_widget(btn)
#        elif dev_type == 'SONOS':
#            for item in sn.list_commands():
#                btn = Button(text=str(item), size_hint_y=None, height=40)
#                btn.bind(on_press=self.send_dev_command)
#                layout.add_widget(btn)
#        elif dev_type == 'TV':
#            for item in tv.list_commands():
#                btn = Button(text=str(item), size_hint_y=None, height=40)
#                btn.bind(on_press=self.send_dev_command)
#                layout.add_widget(btn)
#        elif dev_type == 'SATELLITE' or dev_type == 'ZWave':
#            for item in sat.list_commands(device):
#                btn = Button(text=str(item), size_hint_y=None, height=40)
#                btn.bind(on_press=lambda x, device=device, command=str(item): self.send_dev_command(device, command))
#                layout.add_widget(btn)
        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.popup.add_widget(root)
        self.popup.open()

    def send_dev_command(self, device, command):
        scenes.threadSetDevice(device, command)
        self.popup.dismiss()

    def close_gui(self, *args):
        global running
        running = False
        hbtsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        hbtsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        hbtsocket.sendto(str('empty'),('192.168.192.255',constants.udp_.broadPORT))
        App.get_running_app().stop()
        if constants.gui_.KS: exit()

class TemperaturLabel(Button):
    def pop_up(self, text):
        popup = Popup(title=text,
            size_hint=(None, None), size=(600, 500))
        popup.open()
        cmd = ('SELECT Value, Date FROM Steuerzentrale.HIS_inputs where Name like "%s" and Date >= now() - INTERVAL 1 DAY;') % text
        try:
            con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
            tag_hist = pd.read_sql(cmd, con=con)
            con.close()
            x = tag_hist['Date'].values.tolist()
            y = tag_hist['Value'].values.tolist()
        except:
            x=[0]
            y=[0]
        if not (x and y):
            return
        graph = Graph(xlabel='Time', ylabel='degC', xmin=min(x), xmax=max(x)+10000000000000 , y_ticks_major=5,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, ymin=(min(y)-2.5), ymax=(max(y)+2.5))
        #, xmin=min(x), xmax=max(x)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
#        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        plot.points = zip(x,y)
        graph.add_plot(plot)
        popup.add_widget(graph)
        nachricht = 'Min: ' + str(min(y)) + ' Max: ' + str(max(y))
        graph.add_widget(Label(text=nachricht))


class CO2Label(Label):
    def pop_up(self, *args):
        popup = Popup(title='Test popup',
            size_hint=(None, None), size=(400, 400))
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=25, y_ticks_major=1,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=0, ymax=10)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = (1,2,3)
        y = (5,6,7)
#        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        plot.points = zip(x,y)
        graph.add_plot(plot)
        popup.add_widget(graph)
        nachricht = 'Min: ' + str(min(y)) + ' Max: ' + str(max(y))
        graph.add_widget(Label(text=nachricht))
        popup.open()

class LichtButton(Button):
    pass

class GuiApp(App):
    def build(self):
        self.OpScreen = OpScreen()
        return self.OpScreen

if __name__ == '__main__':
    GuiApp().run()