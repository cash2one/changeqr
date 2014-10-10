#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 20:47:07
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-10 23:26:44

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.conf import settings

from changeqr.wechat.wechat import Wechat

import logging

APP_ID = settings.WEIXIN_API['APP_ID']
APP_SECRET = settings.WEIXIN_API['APP_SECRET']
TOKEN = settings.WEIXIN_API['TOKEN']

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


def test(request):

    from changeqr.tasks.wechattask import download_media
    download_media.delay(9)

    return HttpResponse('Good')
