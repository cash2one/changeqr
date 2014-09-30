#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-30 13:45:48
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-30 14:00:46
import unittest

from wechat import Wechat

APP_ID = 'wx359b54263ab9dca2'
APP_SECRET = 'cb6f31c61fa644783cfab1ae736e5786'


class WeichatTest(unittest.TestCase):

    '''
    '''

    def setUp(self):
        self.wechat = Wechat(token='fake', appid=APP_ID, appsecret=APP_SECRET)

    def test_get_access_token(self):
        self.assertTrue(self.wechat.access_token != None, msg=u'首次获取access_token失败')
        self.assertTrue(self.wechat.access_token != None, msg=u'重复获取access_token失败')

    def test_get_menu(self):
        self.assertTrue(self.wechat.get_menu() != None, msg=u'获取菜单失败')

    def test_gen_menu(self):
    	menu = '''
    	{"menu": {"button": [{"type": "click", "name": "好的", "key": "__CHANGWEI_WEISHOP_KEY", "sub_button": []}]}}
    	'''

if __name__ == '__main__':
    unittest.main()
