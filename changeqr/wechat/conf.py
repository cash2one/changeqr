#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-10-11 21:37:00
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-11 22:26:13

from django.conf import settings
from django.core.cache import cache

import ConfigParser
import time
import logging

logger = logging.getLogger('qrcode')


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

    __TOKEN_KEY = '__TOKEN_CACHE_%s'

    def __init__(self):
        super(RedisTokenCache, self).__init__()

    def get(self, appid):
        return cache.get(self.__TOKEN_KEY % appid)

    def set(self, appid, token):
        cache.set(self.__TOKEN_KEY % appid, token, timeout=self.expire_time)

    def expire(self, appid):
        cache.delete(self.__TOKEN_KEY % appid)

__token_cache_str = getattr(settings, 'TOKEN_CACHE_CLASS', None)

token_cache_clazz = None
if not __token_cache_str:
    logger.info('default token cache class set')
    token_cache_clazz = RedisTokenCache
else:
    try:
        logger.info('token_cache_str set, try to import %s' % __token_cache_str)
        import sys
        ms = __token_cache_str.split('.')
        clazz = ms.pop()
        path = '.'.join(ms)
        __import__(path)
        token_cache_clazz = getattr(sys.modules[path], clazz)
    except Exception, e:
        logger.error('Setting error on key "TOKEN_CACHE_CLASS":  %s, %s' % (__token_cache_str, e))

logger.info(token_cache_clazz)
