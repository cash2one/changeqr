#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-27 10:54:31
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-29 16:12:13


class MessageTypeError(Exception):

    '''
    '''
    pass


class ParseError(Exception):

    '''
    解析微信服务器数据异常
    '''
    pass


class ParamError(Exception):

    '''
    构造参数提供不全异常
    '''
    pass


class APIError(Exception):

    '''
    微信官方API请求出错异常
    '''
    pass
