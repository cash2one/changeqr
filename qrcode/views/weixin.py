#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 20:47:07
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 10:53:17

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from changeqr.wechat.wechat import Wechat
from changeqr.wechat.handler import BaseHandler, handler

APP_ID = 'wx359b54263ab9dca2'
APP_SECRET = 'cb6f31c61fa644783cfab1ae736e5786'
TOKEN = '23d446db1409552373'


@handler.register('event')
class QrcodeHandler(BaseHandler):

    def handle(self, message):
        wechat = message.wechat
        return wechat.reply_text('Good')


@csrf_exempt
def gateway(request):
    wechat = Wechat(token=TOKEN, appid=APP_ID, appsecret=APP_SECRET)

    ret = wechat.parse(request.GET, request.body, request.method)

    return HttpResponse(ret)
