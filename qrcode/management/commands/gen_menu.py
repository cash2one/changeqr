#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-15 14:20:18
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-15 14:25:30

from django.core.management.base import BaseCommand
from django.conf import settings

from changeqr.wechat.wechat import Wechat


class Command(BaseCommand):

    def handle(self, *args, **options):

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

        try:
            weixin = settings.WEIXIN_API

            wechat = Wechat(
                token=weixin['TOKEN'], appid=weixin['APP_ID'], appsecret=weixin['APP_SECRET'])
            ret = wechat.create_menu(menu)

            print ret
        except Exception, e:
            print e
