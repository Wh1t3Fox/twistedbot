#!/usr/bin/env python

import requests
import urllib
from bs4 import BeautifulSoup

class Webpage(object):

    def __init__(self, url):
        self.get_info(url)

    def get_info(self, url):
        resp = urllib.urlopen(url)
        url = resp.url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        self.title = str(soup.title.string)
