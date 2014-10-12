#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 20:47:07
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-12 14:34:36

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


def enqueue(request, id):

    from changeqr.tasks.wechattask import download_media
    download_media.delay(id)

    return HttpResponse('Enqueue success')


def menu(request):
    menu = u'''
    {
        "button": [{
            "name": "扫码",
            "type": "scancode_waitmsg",
            "key": "scancode",
            "sub_button": []
        }, {
            "name": "帮助",
            "type": "click",
            "key": "help",
            "sub_button": []
        }]
    }
    '''.encode('utf-8')
    from changeqr.wechat.wechat import Wechat

    wechat = Wechat(token='token', appid=APP_ID, appsecret=APP_SECRET)
    ret = wechat.create_menu(menu)

    logger.info(ret)

    return HttpResponse(ret)
