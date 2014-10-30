#!/usr/bin/env python

import re
import requests
import urllib
from bs4 import BeautifulSoup

class Webpage(object):

    def __init__(self, url):
        self.get_info(url)

    def get_info(self, url):
        resp = urllib.urlopen(url)
        r = requests.get(resp.url)
        soup = BeautifulSoup(r.text)
        self.title = re.sub(r'\r|\n','',str(soup.title.string))
