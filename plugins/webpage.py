#!/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup

class Webpage(object):

    def __init__(self, url):
        self.get_info(url)

    def sanitize_url(self, text):
        return re.sub(r'[\r|\n|\s]*','',text)

    def sanitize_text(self, text):
        return re.sub(r'[\r|\n]*','',text).strip()

    def get_info(self, url):
        r = requests.get(self.sanitize_url(url))
        soup = BeautifulSoup(r.text)
        self.title = self.sanitize_text(str(soup.title.string))
