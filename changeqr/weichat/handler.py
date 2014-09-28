#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-27 12:03:29
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-28 20:48:25

import time

from messages import WechatMessage, TextMessage
from exception import MessageTypeError


class BaseHandler():

    '''
    消息处理类基类
    '''

    def handle(self, message):
        pass


class HandlerRegister():

    def __init__(self):
        self.handlers = {}

    def register(self, type, level=0):
        '''
        注册一个处理类，并加入到处理队列中
        TOFIX: 最好使用优先级队列？
        '''

        def handler_wrapper(handler):
            self.handlers[type] = self.handlers.pop(type, [])
            if level > 0:
                self.handlers[type].insert(0, handler)
            else:
                self.handlers[type].append(handler)

            return handler
        return handler_wrapper

    def handle(self, message):
        if not isinstance(message, WechatMessage):
            raise MessageTypeError()

        handlers = self.handlers.get(message.msgtype, [])
        ret = None
        for handler in handlers:
            ret = handler().handle(message)
            if ret:
                return ret


handler = HandlerRegister()
