#!/usr/bin/env python

import hashlib


class Hash(object):

    def __init__(self, alg, data):
        self.compute_hash(alg, data)

    def compute_hash(self, alg, data):
        h = hashlib.new(alg)
        h.update(data)
        self.result = h.hexdigest()
