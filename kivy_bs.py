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
import os
import datetime


class ScreenSaver_handler(object):
    def __init__(self):
        self.last_event = datetime.datetime.now()
        Window.bind(on_motion=self.on_motion)
        event = Clock.schedule_interval(self.slideshow, .5)
        event()
        self.ss_on = False
        Logger.info("init done")

    def slideshow(self, *args):
        if datetime.datetime.now() - self.last_event > datetime.timedelta(hours=0, minutes=0, seconds=10):
            if not self.ss_on:
                self.backlight(0)
                Logger.info("screen off")
                self.ss_on = True

    def on_motion(self, *args, **kwargs):
        self.last_event = datetime.datetime.now()
        self.backlight(100)
        Logger.info("screen on")
        self.ss_on = False

    def backlight(self, value):
        exectext = 'echo %s > /sys/class/backlight/rpi_backlight/brightness' % (value)
        os.system(exectext) 

class YourApp(App):
    def build(self):
#        Clock.schedule_interval(ssh.slideshow, .5)
        root_widget = BoxLayout(orientation='vertical')

        output_label = Label(size_hint_y=1)  

        button_symbols = ('1', '2', '3',
                          '4', '5', '6',
                          '7', '8', '9',
                          '*', '0', 'Del')

        button_grid = GridLayout(cols=3, size_hint_y=2) 
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        enter_button = Button(text='enter', size_hint_y=None,
                              height=100)

        def print_button_text(instance):
            if 'Eingabe' in output_label.text:
                output_label.text = ''            
            output_label.text += instance.text
            
        def delete_key(instance):
            if 'Eingabe' in output_label.text:
                output_label.text = ''            
            output_label.text = output_label.text[:-1]            
            
        for button in button_grid.children[1:]:  # note use of the
                                             # `children` property
            button.bind(on_press=print_button_text)
            
        button_grid.children[0].bind(on_press=delete_key)

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
            if output_label.text == '1234':
                output_label.text = 'Eingabe OK'
            else:
                output_label.text = 'Eingabe Falsch'
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
