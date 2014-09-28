#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-28 12:08:33
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-28 16:03:32

import hashlib
# import requests
import time
import json

from xml.dom import minidom

from messages import messager
from handler import handler


class Wechat():

    '''
    微信基本功能类
    '''

    def __init__(self, token=None, appid=None, appsecret=None):
        '''
        access_token 使用redis进行缓存，key为appid，每次获取后将自动缓存到redis至过期
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        '''
        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret

        self.__handler = handler

    def validate(self):
        '''
        验证微信消息真实性
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return: 通过验证返回 True, 未通过验证返回 False
        '''
        self._check_token()

        if not self._timestamp or not self._nonce or not self._signature:
        	return False

        tmp_list = [self.__token, self._timestamp, self._nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        if self._signature == hashlib.sha1(tmp_str).hexdigest():
            return True
        else:
            return False

    def parse(self, get, data):
        '''
        解析微信服务器发送过来的数据并保存类中
        :param data: HTTP Request 的 Body 数据
        :raises ParseError: 解析微信服务器数据错误, 数据不合法
        '''

        self._signature = get.get('signature', None)
        self._timestamp = get.get('timestamp', None)
        self._nonce = get.get('nonce', None)
        self._echostr = get.get('echostr', None)

        # 检查签名有效性
        if not self.validate():
            # raise Exception('Sign invalid')
            pass

        # 解析消息
        result = {}
        if type(data) == unicode:
            data = data.encode('utf-8')
        elif type(data) == str:
            pass
        else:
            raise ParseError()

        try:
            doc = minidom.parseString(data)
        except Exception:
            raise ParseError()

        params = [ele for ele in doc.childNodes[0].childNodes
                  if isinstance(ele, minidom.Element)]

        for param in params:
            if param.childNodes:
                text = param.childNodes[0]
                result[param.tagName] = text.data
        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()

        message_type = messager.get_message_class(result['type'])
        self.__message = message_type(result)

        # 处理消息
        return self.__handler.handle(self.__message)

    def _check_token(self):
        '''
        检查 Token 是否存在
        :raises NeedParamError: Token 未初始化
        '''
        if not self.__token:
            raise NeedParamError('Token未初始化')

    def _check_appid_appsecret(self):
        '''
        检查 AppID 和 AppSecret 是否存在
        :raises NeedParamError: AppID 或 AppSecret 未初始化
        '''
        if not self.__appid or not self.__appsecret:
            raise NeedParamError('appid 或 appsecret 未初始化')
