#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-28 12:06:58
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-28 20:46:54

import time

from handler import handler, BaseHandler
from messages import TextMessage
from reply import ImageReply, TextReply
from wechat import Wechat


@handler.register('text')
class SystemHandler(BaseHandler):

    def handle(self, message):
        reply = ImageReply(message=message, media_id='_media_id_')
        return reply.render()


@handler.register('event')
@handler.register('text')
class AutoReplyHandler(BaseHandler):

    def handle(self, message):
        reply = TextReply(message=message, content=u'Welcome')
        return reply.render()


wechat = Wechat(token='token')
ret = wechat.parse({
    'signature': 'abc',
    'timestamp': '1234',
    'nonce': '1234'
}, '''
<xml><ToUserName><![CDATA[gh_95d589f53556]]></ToUserName>
<FromUserName><![CDATA[oPfCTuMfbVNck6fjMjUUwGEhkWCE]]></FromUserName>
<CreateTime>1409552501</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[__CHANGWEI_WEIDIAN_KEY]]></EventKey>
</xml>''')


print ret
