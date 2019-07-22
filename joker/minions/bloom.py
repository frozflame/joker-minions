#!/usr/bin/env python3
# coding: utf-8

import mmh3
from bitarray import bitarray

from joker.minions import utils


class BloomFilter(object):
    def __init__(self, size, seed=3):
        self.size = size
        self.seed = seed
        self.bitarr = bitarray(size)
        self.bitarr ^= self.bitarr

    def _compute_hash(self, item):
        return mmh3.hash(item, self.seed) % self.size

    def __setitem__(self, key, value):
        idx = self._compute_hash(key)
        self.bitarr[idx] = bool(value)

    def __getitem__(self, key):
        idx = self._compute_hash(key)
        return self.bitarr[idx]


class BloomMixin(object):
    def __init__(self, size, seed=3):
        self.bloom = BloomFilter(size, seed)

    def query(self, line):
        cmd, key = utils.split(line)
        cmd = cmd.lower()
        if cmd == b'get':
            return self.bloom[key]
        if cmd == b'set':
            self.bloom[key] = True
        if cmd == b'del':
            self.bloom[key] = False


class BloomServer(BloomMixin, utils.ServerBase):
    pass


class PipedBloomServer(BloomMixin, utils.PipedServerBase):
    pass
