# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:58:42 2016

@author: chuckle
"""

import constants
import git

def git_update():
    g = git.cmd.Git()
    g.pull()
    constants.run = False