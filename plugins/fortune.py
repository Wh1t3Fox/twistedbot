#!/usr/bin/env python

import subprocess

class Fortune(object):

    def __init__(self):
        self.get_fortune()

    def get_fortune(self):
        proc = subprocess.Popen("fortune", stdout=subprocess.PIPE, shell=False)
        self.msg = proc.communicate()[0].replace("\n", " ")
