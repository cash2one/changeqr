#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 19:25:40
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 10:53:06

from django.db import models

import string
import random


def random_str(length=11):
    '''
    生成随机字符串，长度为 len
    ;param: len 字符串长度
    '''

    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(length))

CODE_STATUS = (
    (0, '等待激活'),
    (1, '等待输入'),
    (2, '正在使用'),  # 已经录入内容
    (3, '冻结'),
)


class Qrcode(models.Model):

    '''
    二维码字符串 20 位
    前缀 4位 + 连接符 1位 + 二维码 15位
    '''

    # 前缀，用于区分用户/使用场景等
    prefix = models.CharField(blank=False, max_length=4)
    # 二维码字段，用于区分不同二维码
    code = models.CharField(blank=False, unique=True, max_length=15)
    # 完整二维码串
    full = models.CharField(blank=False, unique=True, max_length=20)

    status = models.IntegerField(
        default=0, choices=CODE_STATUS, verbose_name='二维码状态')

    create_at = models.DateTimeField(
        default=datetime.now, verbose_name=u'创建时间')
    active_at = models.DateTimeField(blank=True, verbose_name=u'激活时间')
    used_at = models.DateTimeField(blank=True, verbose_name=u'使用时间')

    visit_count = models.IntegerField(default=0, verbose_name=u'访问次数')

    def __unicode__(self):
        return self.full

    @staticmethod
    def create(prefix=''):
        '''
        创建新的二维码
        :param prefix 二维码前缀
        '''
        if len(prefix) != 4:
            return None
        qr = Qrcode()

        code = random_str(length=15)

        qr.prefix = prefix
        qr.code = code

        qr.full = '-'.join([prefix, code])
        try:
            qr.save()
        except Exception, e:
            return Qrcode.create(prefix=prefix)

        return qr

    @staticmethod
    def createmanay(prefix=''):
        pass


class SubQrcode(models.Model):

    '''
    适用于一次保存，多次使用的场景，同时保证每个二维码都是唯一的
    前缀 4位 + 连接符 1位 + 二维码 15位 + 连接符 1位 + 后缀 5位
    理论上每个二维码可以拥有 (26+26+10)**5 个子二维码
    '''

    qrcode = models.ForeignKey(Qrcode)  # 所属的父级二维码
    postfix = models.CharField(blank=False, unique=True, max_length=5)
    full = models.CharField(blank=False, unique=True, max_length=26)

    status = models.IntegerField(
        default=0, choices=CODE_STATUS, verbose_name='二维码状态')

    create_at = models.DateTimeField(
        default=datetime.now, verbose_name=u'创建时间')
    active_at = models.DateTimeField(blank=True, verbose_name=u'激活时间')
    used_at = models.DateTimeField(blank=True, verbose_name=u'使用时间')

    visit_count = models.IntegerField(default=0, verbose_name=u'访问次数')

    @staticmethod
    def createmanay(prefix=None):
        pass
