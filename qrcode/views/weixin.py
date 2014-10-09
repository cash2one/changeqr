#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 20:47:07
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 21:05:38

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from changeqr.wechat.wechat import Wechat

import logging

APP_ID = 'wx359b54263ab9dca2'
APP_SECRET = 'cb6f31c61fa644783cfab1ae736e5786'
TOKEN = '23d446db1409552373'

logger = logging.getLogger('qrcode')


@csrf_exempt
def gateway(request):
    wechat = Wechat(token=TOKEN, appid=APP_ID, appsecret=APP_SECRET)

    try:
        ret = wechat.parse(request.GET, request.body, request.method)
    except Exception, e:
        logger.error(e)
        import traceback
        logger.error(traceback.print_exc())
        logger.debug(request.body)
        return HttpResponse('')

    return HttpResponse(ret)
