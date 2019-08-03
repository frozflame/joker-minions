#!/usr/bin/env python3
# coding: utf-8

from joker.minions import utils


class CacheMixin(object):
    val_pop = b'#'
    val_none = b''

    def __init__(self, data=None):
        self.data = {} if data is None else data

    def lookup(self, key, val):
        if val == self.val_pop:
            return self.data.pop(key, self.val_none)
        rv = self.data.get(key, self.val_none)
        if val:
            self.data[key] = val
        return rv


class CacheServer(CacheMixin, utils.ServerBase):
    pass


class PipedCacheServer(CacheMixin, utils.PipedServerBase):
    pass
