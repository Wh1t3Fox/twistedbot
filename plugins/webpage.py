#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

class Webpage(object):

    def __init__(self, url):
        self.get_info(url)

    def get_info(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        self.title = str(soup.title.string)
