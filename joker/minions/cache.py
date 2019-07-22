#!/usr/bin/env python3
# coding: utf-8

from joker.minions import utils


class CacheMixin(object):
    def __init__(self):
        self.data = {}

    def query(self, line):
        key, val = utils.split(line)
        if val == b'%':
            return self.data.pop(key, b'%')
        rv = self.data.get(key, b'%')
        if val:
            self.data[key] = val
        return rv


class CacheServer(CacheMixin, utils.ServerBase):
    pass


class PipedCacheServer(CacheMixin, utils.PipedServerBase):
    pass

