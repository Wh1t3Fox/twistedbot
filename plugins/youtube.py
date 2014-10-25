#!/usr/bin/env python

import requests
import json

class Youtube(object):

    def __init__(self, id):
        self.url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
        self.lookup(self.url)

    def lookup(self, url):
        json_string = requests.get(url).json()
        self.title = str(json_string['entry']['title']['$t'])
        self.author = str(json_string['entry']['author'][0]['name']['$t'])
        self.description = str(json_string['entry']['media$group']['media$description']['$t'])
