#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-09-27 10:23:54
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 14:32:24


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
        return self.message_types.get(type, UnknownMessage)

messager = MessageRegister()


class WechatMessage(dict):

    def __init__(self, message):
        self.id = int(message.pop('MsgId', 0))
        self.touser = message.pop('ToUserName', None)
        self.fromuser = message.pop('FromUserName', None)
        self.createtime = int(message.pop('CreateTime', 0))
        self.raw = message.pop('raw', '')
        self.update(message)
        self.msgtype = message.pop('type', 'unknow')

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
        # click, view, scancode_push, scancode_waitmsg, pic_sysphoto, pic_photo_or_album, pic_weixin, location_select
        self.event = message.pop('Event')
        self.eventkey = message.pop('EventKey')
        self.ticket = message.pop('Ticket', None)

        self.latitude = message.pop('Latitude', None)
        self.longtitude = message.pop('Longtitude', None)
        self.precision = message.pop('Precision', None)

        self.scaninfo = message.pop('ScanCodeInfo', None)
        if self.scaninfo:
            self.scanresult = self.scaninfo['ScanResult']
            self.scantype = self.scaninfo['ScanType']

        self.picinfo = message.pop('SendPicsInfo', None)
        if self.picinfo:
            self.piccount = self.picinfo['Count']
            self.piclist = self.picinfo['PicList']

        self.locinfo = message.pop('SendLocationInfo', None)
        if self.locinfo:
            self.location_x = self.locinfo['Location_X']
            self.location_y = self.locinfo['Location_Y']
            self.locscale = self.locinfo['Scale']
            self.loclabel = self.locinfo['Label']
            self.locpoi = self.locinfo['Poiname']

        super(EventMessage, self).__init__(message)
