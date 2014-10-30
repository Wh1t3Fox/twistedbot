#!/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup

class Webpage(object):

    def __init__(self, url):
        self.get_info(url)

    def sanitized(self, text):
        return re.sub(r'\r|\n','',text)

    def get_info(self, url):
        r = requests.get(self.sanitized(url))
        soup = BeautifulSoup(r.text)
        self.title = self.sanitized(str(soup.title.string))
