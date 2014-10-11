#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-30 11:17:39
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 13:57:12

import ConfigParser
import time


class TokenCache(object):

    def __init__(self):
        self.expire_time = 7200

    def get(self, appid):
        return None

    def set(self, appid, token):
        pass

    def expire(self, appid):
        pass


class FileTokenCache(TokenCache):

    def __init__(self, cfg='cache.cfg'):
        self.fp = cfg

        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.config.read(self.fp)

        self.save()

        super(FileTokenCache, self).__init__()

    def get(self, appid):
        try:
            token = self.config.get('token', appid)
        except:
            return None
        array = token.split('|')
        if int(time.time()) - int(array[1]) > self.expire_time:
            self.expire(appid)
            return None
        return array[0]

    def set(self, appid, token):
        self.config.set('token', appid, '%s|%d' % (token, int(time.time())))
        self.save()

    def expire(self, appid):
        self.config.remove_option('token', appid)
        self.save()

    def save(self):
        try:
            self.config.set('token', 'last_update', int(time.time()))
        except:
            self.config.add_section('token')
            self.config.set('token', 'last_update', int(time.time()))

        self.config.write(open(self.fp, 'w'))


class RedisTokenCache(TokenCache):
    pass

token_cache_clazz = FileTokenCache
