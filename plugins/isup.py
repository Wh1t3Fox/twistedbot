#!/usr/bin/env python

import requests

class ISUP(object):

    def __init__(self, url):
        self.check_status(url)

    def check_status(self, url):
        response = requests.get('http://www.isup.me/'+url).text
        if response.find("It's just you.") != -1:
            self.status = "[+] {0} is UP".format(url)
        else:
            self.status = "[-] {0} is DOWN".format(url)
