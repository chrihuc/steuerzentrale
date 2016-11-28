# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:58:42 2016

@author: chuckle
"""

import constants
import git
from alarmevents import alarm_event

aes = alarm_event()

class internal:
    
    def __init__ (self):
        pass

    def list_commands(self):
        return ['Update']
        
    def execute(self, commd):
        if commd == 'Update':
            self.git_update()
        
    def git_update(self):
        g = git.cmd.Git()
        g.pull()
        g.reset('--hard')
        print "Update done, exiting"
        aes.new_event(description="Update performed, restarting", prio=1)
        constants.run = False