# -*- coding: utf-8 -*-
"""
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.base import runTouchApp

from kivy.uix.modalview import ModalView
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image,AsyncImage

import os
import datetime
from outputs.mqtt_publish import mqtt_pub
import constants
import random

from inputs.mqtt_kivy_client import MqttClient

class PictureFrame(ModalView):

    def __init__(self, **kwargs):
        super(PictureFrame, self).__init__(**kwargs)
        self.bind(on_touch_down=self.dismiss)
        self.base_dir = constants.gui_.Bilder
        self.imgs = [os.path.join(self.base_dir, img) for img in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, img))]
        self.carousel = Carousel(direction='right', loop=True)
#        random.shuffle(self.imgs)
        for img in self.imgs:
            image = Image(source=img)
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
        self.imgs = [os.path.join(self.base_dir, img) for img in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, img))]
        random.shuffle(self.imgs)
        self.carousel.clear_widgets()
        for img in self.imgs:
            image = AsyncImage(source=img, nocache=False)
            self.carousel.add_widget(image)        
        self.open()
        self.clock_event = Clock.schedule_interval(self.carousel.load_next, self.delay)

class ScreenSaver_handler(object):
    def __init__(self):
        self.last_event = datetime.datetime.now()
        Window.bind(on_motion=self.on_motion)
        event = Clock.schedule_interval(self.slideshow, .5)
        event()
        topics = ["Settings/#"]
        self.mq_cli = MqttClient("192.168.192.2", topics, self.mqtt_on_mes)
#        self.mq_cli.connect()          
        self.ss_on = False
        self.pic_frame = PictureFrame()
        Logger.info("init done")

    def slideshow(self, *args):
        if datetime.datetime.now() - self.last_event > datetime.timedelta(hours=0, minutes=0, seconds=10):
            if not self.ss_on:
                if self.mq_cli.status == None or self.mq_cli.status == "Wach":
                    self.pic_frame.start_show()
                else:
                    self.backlight(0)
                Logger.info("screen off")
                self.ss_on = True

    def on_motion(self, *args, **kwargs):
        self.last_event = datetime.datetime.now()
        self.backlight(100)
        self.pic_frame.dismiss()
        Logger.info("screen on")
        self.ss_on = False

    def backlight(self, value):
        exectext = 'echo %s > /sys/class/backlight/rpi_backlight/brightness' % (value)
        os.system(exectext) 
    
    def mqtt_on_mes(self, topic, m_in):
#        print(topic)
        if topic == "Settings/Status":
            if m_in['Value'] == "Wach":
                self.backlight(100)
                self.pic_frame.start_show()
            else:
                self.backlight(0)
                self.pic_frame.dismiss()                

class YourApp(App):
    def build(self):
#        Clock.schedule_interval(ssh.slideshow, .5)
        root_widget = BoxLayout(orientation='vertical')

        output_label = Label(size_hint_y=1)  

        button_symbols = ('1', '2', '3',
                          '4', '5', '6',
                          '7', '8', '9',
                          'Del', '0', 'Enter')

        button_grid = GridLayout(cols=3, size_hint_y=2) 
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        enter_button = Button(text='', size_hint_y=None,
                              height=100)

        def print_button_text(instance):
            liste = ['Hallo', 'aus', 'Eingabe']
            if any([True for i in liste if i in output_label.text]):
                output_label.text = ''            
            output_label.text += instance.text
            
        def delete_key(instance):
            liste = ['Hallo', 'aus', 'Eingabe']
            if any([True for i in liste if i in output_label.text]):
                output_label.text = ''            
            output_label.text = output_label.text[:-1]            
            
        for button in button_grid.children[3:]:  # note use of the
                                             # `children` property
            button.bind(on_press=print_button_text)
        
        button_grid.children[1].bind(on_press=print_button_text)
        button_grid.children[2].bind(on_press=delete_key)

        def resize_label_text(label, new_height):
            label.font_size = 0.5*label.height
        output_label.bind(height=resize_label_text)

#        def evaluate_result(instance):
#            try:
#                output_label.text = str(eval(output_label.text))
#            except SyntaxError:
#                output_label.text = 'Python syntax error!'
#        button_grid.children[0].bind(on_press=evaluate_result)

        def clear_label(instance):
            if output_label.text in constants.pins.besucher:
                output_label.text = 'Hallo Besucher'
                command = {'Szene':'Besuch'}
                mqtt_pub("Command/Szene/Besuch", command)
                print("besucher")
            elif output_label.text in constants.pins.bewohner:
                output_label.text = 'Alarmanlage aus'
                command = {'Szene':'AlarmanlageAus'}
                mqtt_pub("Command/Szene/AlarmanlageAus", command)   
                command = {'Szene':'Wach'}
                mqtt_pub("Command/Szene/Wach", command)   
                print("bewohner")
            else:
                output_label.text = 'Eingabe Falsch'
                command = {'Szene':'FalscherPin'}
                mqtt_pub("Command/Szene/FalscherPin", command)                 
                
        button_grid.children[0].bind(on_press=clear_label)                
        enter_button.bind(on_press=clear_label)

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(enter_button)
        return root_widget



test = YourApp()
ssh = ScreenSaver_handler() 
#ssh.slideshow()
test.run()
#runTouchApp()
