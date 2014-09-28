#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-09-27 10:23:54
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-28 17:09:26


class MessageRegister():

    def __init__(self):
        self.message_types = {}

    def register(self, type):
        def message_wrapper(msg):
            self.message_types[type] = msg
            msg.msgtype = type
            return msg
        return message_wrapper

    def get_message_class(self, type):
        return self.message_types.pop(type, UnknownMessage)

messager = MessageRegister()


class WechatMessage(dict):

    def __init__(self, message):
        self.id = int(message.pop('MsgId', 0))
        self.touser = message.pop('ToUserName', None)
        self.fromuser = message.pop('FromUserName', None)
        self.createtime = int(message.pop('CreateTime', 0))
        self.update(message)

    def from_xml(self, xml):
        pass

    def to_xml(self):
        return ''


class UnknownMessage(WechatMessage):

    def __init__(self, message):
        self.msgtype = 'unknown'
        super(UnknownMessage, self).__init__(message)


@messager.register('text')
class TextMessage(WechatMessage):

    def __init__(self, message):
        self.content = message.pop('Content', '')
        super(TextMessage, self).__init__(message)


@messager.register('image')
class ImageMessage(WechatMessage):

    def __init__(self, message):
        self.mediaid = message.pop('MediaId', '')
        self.picurl = message.pop('PicUrl', '')
        super(ImageMessage, self).__init__(message)


@messager.register('voice')
class VoiceMessage(WechatMessage):

    def __init__(self, message):
        self.mediaid = message.pop('MediaId', '')
        self.format = message.pop('Format', 'amr')
        super(VoiceMessage, self).__init__(message)


@messager.register('video')
class VideoMessage(WechatMessage):

    def __init__(self, message):
        self.mediaid = message.pop('MediaId', '')
        self.thumbmediaid = message.pop('ThumbMediaId', '')
        super(VideoMessage, self).__init__(message)


@messager.register('location')
class LocationMessage(WechatMessage):

    def __init__(self, message):
        self.latitude = message.pop('Location_X', '')
        self.longtitude = message.pop('Location_Y', '')
        self.scale = message.pop('Scale', '')
        self.label = message.pop('Label', '')
        super(LocationMessage, self).__init__(message)


@messager.register('link')
class LinkMessage(WechatMessage):

    def __init__(self, message):
        self.title = message.pop('Title', '')
        self.description = message.pop('Description', '')
        self.url = message.pop('Url', '')
        super(LinkMessage, self).__init__(message)


@messager.register('event')
class EventMessage(WechatMessage):

    def __init__(self, message):
        self.event = message.pop('Event')
        self.eventkey = message.pop('EventKey')

        super(EventMessage, self).__init__(message)
