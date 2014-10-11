#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 19:25:40
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-11 17:45:02

from django.db import models

import string
import random
from datetime import datetime

CODE_STATUS = (
    (0, '等待激活'),
    (1, '空白二维码'),
    (4, '正在编辑'),
    (2, '正在使用'),  # 已经录入内容
    (3, '冻结'),
)


def random_str(length=11):
    '''
    生成随机字符串，长度为 len
    ;param: len 字符串长度
    '''

    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(length))


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
            # TODO: 如何对生成的二维码去重
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
    active_at = models.DateTimeField(
        blank=True, null=True, verbose_name=u'激活时间')
    used_at = models.DateTimeField(blank=True, null=True, verbose_name=u'使用时间')

    visit_count = models.IntegerField(default=0, verbose_name=u'访问次数')

    @staticmethod
    def createmanay(prefix=None):
        pass


class CodeContent(models.Model):

    '''
    一个二维码对应的媒体类，可以包含1-3个 图片、视频、音频
    '''

    CONTENT_STATUS = (
        (0, 'Created'),  # 创建
        (1, 'Interactive'),  # 正在交互
        (2, 'Confirmed'),  # 已确认
        (3, 'Downloaded'), # 媒体已下载
        (4, 'Canceled'),  # 撤销
    )

    qrcode = models.OneToOneField(Qrcode, blank=False)
    # 操作者 微信公众 ID
    uid = models.CharField(max_length=30)

    text = models.CharField(max_length=400)

    image_count = models.IntegerField(default=0)  # MAX 6

    voice_count = models.IntegerField(default=0)  # MAX 1

    video_count = models.IntegerField(default=0)  # MAX 1

    last_media = models.IntegerField(null=True, blank=True) # 最近一次操作增加的内容，用于撤销

    status = models.IntegerField(default=0, choices=CONTENT_STATUS)

    last_update = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.last_update = datetime.now()
        super(CodeContent, self).save(*args, **kwargs)

    def accept_more(self, type=100):
        if type == 1:
            return self.voice_count < 1
        elif type == 2:
            return self.image_count < 6
        elif type == 3:
            return False
            # return self.video_count < 1
        elif type == 0:
            return not self.text
        else:
            return self.image_count < 6 or self.voice_count < 1 and self.text

    def incr(self, media_type):
        if media_type == 1:
            self.voice_count += 1
        elif media_type == 2:
            self.image_count += 1
        elif media_type == 3:
            self.video_count += 1
        else:
            return

        self.last_media = media_type
        self.save()

    def decr(self, media_type):
        if media_type == 1:
            self.voice_count -= 1
        elif media_type == 2:
            self.image_count -= 1
        elif media_type == 3:
            self.video_count -= 1
        else:
            return

        self.last_media = None
        self.save()



class CodeMedia(models.Model):

    '''
    一条媒体信息，包括图片、视频、音频
    '''
    MEDIA_TYPE = (
        (0, '未知类型'),
        (1, 'voice'),
        (2, 'pic'),
        (3, 'video'),
    )

    relate_to = models.ForeignKey(CodeContent, blank=False)

    media_type = models.IntegerField(default=0, choices=MEDIA_TYPE)

    media_id = models.CharField(blank=False, max_length=64)

    picurl = models.CharField(blank=True, null=True, max_length=200)

    vformat = models.CharField(blank=True, null=True, max_length=5)

    thumbmediaid = models.CharField(blank=True, null=True, max_length=64)

    confirmed = models.BooleanField(default=False)

    url = models.CharField(max_length=100, default='')

    def ext_name(self):
        if self.media_type == 1:
            return self.vformat
        elif self.media_type == 2:
            return 'jpg'
        elif self.media_type == 3:
            return 'mp4'
        return ''
