# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:58:42 2016

@author: chuckle
"""

import constants
import git

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
        print "Update done, exiting"
        constants.run = False