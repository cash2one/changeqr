#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-08 19:25:40
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-15 14:37:19

from django.db import models

import string
import random
import hashlib
from datetime import datetime

CODE_STATUS = (
    (0, '等待激活'),
    (1, '空白二维码'),
    (4, '正在编辑'),
    (2, '正在使用'),  # 已经录入内容
    (3, '冻结'),
)


def checksum(origin):
    '''
    简单校验
    '''
    m = hashlib.md5()
    m.update(origin)
    return '%s%s' % (origin, m.hexdigest()[8:9])


def checksum_valid(origin):
    '''
    '''
    tovalid = origin[0:-1]
    checksum = origin[-1:0]

    m = hashlib.md5()
    m.update(tovalid)
    return checksum == m.hexdigest()[8:9]


def random_str(length=11):
    '''
    生成随机字符串，长度为 len
    ;param: len 字符串长度
    '''

    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(length))


class Qrprefix(models.Model):

    '''
    二维码前缀 4 位，用于管理二维码
    '''
    code = models.CharField(
        blank=False, unique=True, max_length=4, verbose_name=u'内容')

    # 用于保存不知道啥
    title = models.CharField(
        default=u'空白前缀', max_length=50, verbose_name=u'标题')

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = '二维码前缀'
        verbose_name_plural = '二维码前缀'

    @staticmethod
    def create(code=None, title=''):
        '''
        创建新的前缀
        '''
        prefix = Qrprefix()

        prefix.title = title

        if not code:
            prefix.code = random_str(length=4)
        else:
            prefix.code = code

        try:
            prefix.save()
        except:
            if code:
                raise Exception(u'该前缀已经被使用')
            return Qrprefix.create(title=title)

        return prefix


class Qrcode(models.Model):

    '''
    二维码字符串 20 位
    前缀 4位 + 二维码类别 1位 + 二维码 14位 + 校验码 1位
    '''

    # 前缀，用于区分用户/使用场景等
    prefix = models.CharField(blank=False, max_length=4, verbose_name=u'前缀')
    # 二维码类别
    ctype = models.CharField(blank=False, max_length=1, verbose_name=u'类别')
    # 二维码字段，用于区分不同二维码
    code = models.CharField(blank=False, max_length=14, verbose_name=u'内容')
    # 完整二维码串
    full = models.CharField(
        blank=False, unique=True, max_length=20, verbose_name=u'完整')

    status = models.IntegerField(
        default=0, choices=CODE_STATUS, verbose_name='二维码状态')

    create_at = models.DateTimeField(
        default=datetime.now, verbose_name=u'创建时间')
    active_at = models.DateTimeField(
        blank=True, null=True, verbose_name=u'激活时间')
    used_at = models.DateTimeField(blank=True, null=True, verbose_name=u'使用时间')

    visit_count = models.IntegerField(default=0, verbose_name=u'访问次数')

    def __unicode__(self):
        return self.full

    class Meta:
        verbose_name = '二维码'
        verbose_name_plural = '二维码'

    @staticmethod
    def create(prefix, ctype='0'):
        '''
        创建新的二维码
        :param prefix 二维码前缀
        '''
        qr = Qrcode()

        code = random_str(length=14)

        qr.prefix = prefix
        qr.code = code
        qr.ctype = ctype

        qr.full = checksum(''.join([prefix, ctype, code]))
        try:
            qr.save()
        except Exception, e:
            return Qrcode.create(prefix, ctype=ctype)

        return qr


class Subcode(models.Model):

    '''
    适用于一次保存，多次使用的场景，同时保证每个二维码都是唯一的
    前缀 4位 + 二维码类别 1位 + 二维码 15位 + 连接符 1位 + 后缀 5位
    理论上每个二维码可以拥有 (26+26+10)**5 个子二维码
    '''

    qrcode = models.ForeignKey(Qrcode, verbose_name=u'二维码')  # 所属的父级二维码
    postfix = models.CharField(
        blank=False, unique=True, max_length=5, verbose_name=u'后缀')
    full = models.CharField(
        blank=False, unique=True, max_length=26, verbose_name=u'完整码')

    status = models.IntegerField(
        default=0, choices=CODE_STATUS, verbose_name='二维码状态')

    create_at = models.DateTimeField(
        default=datetime.now, verbose_name=u'创建时间')
    active_at = models.DateTimeField(
        blank=True, null=True, verbose_name=u'激活时间')
    used_at = models.DateTimeField(blank=True, null=True, verbose_name=u'使用时间')

    visit_count = models.IntegerField(default=0, verbose_name=u'访问次数')

    def __unicode__(self):
        return self.full

    class Meta:
        verbose_name = '二维码子码'
        verbose_name_plural = '二维码子码'


class CodeContent(models.Model):

    '''
    一个二维码对应的媒体类，可以包含1-3个 图片、视频、音频
    '''

    CONTENT_STATUS = (
        (0, 'Created'),  # 创建
        (1, 'Interactive'),  # 正在交互
        (2, 'Confirmed'),  # 已确认
        (3, 'Downloaded'),  # 媒体已下载
        (4, 'Canceled'),  # 撤销
    )

    qrcode = models.OneToOneField(Qrcode, blank=False, verbose_name=u'二维码')
    # 操作者 微信公众 ID
    uid = models.CharField(max_length=30, verbose_name=u'操作者ID')

    text = models.CharField(max_length=400, blank=True, null=True, verbose_name=u'文本内容')

    image_count = models.IntegerField(default=0, verbose_name=u'图片数量')  # MAX 6

    voice_count = models.IntegerField(default=0, verbose_name=u'音频数量')  # MAX 1

    video_count = models.IntegerField(default=0, verbose_name=u'视频数量')  # MAX 1

    last_media = models.IntegerField(
        null=True, blank=True, verbose_name=u'最后修改')  # 最近一次操作增加的内容，用于撤销

    status = models.IntegerField(
        default=0, choices=CONTENT_STATUS, verbose_name=u'状态')

    last_update = models.DateTimeField(
        default=datetime.now, verbose_name=u'最后更新')

    def __unicode__(self):
        return self.qrcode

    class Meta:
        verbose_name = '二维码媒体内容'
        verbose_name_plural = '二维码媒体内容'

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

    relate_to = models.ForeignKey(
        CodeContent, blank=False, verbose_name=u'所属内容')

    media_type = models.IntegerField(
        default=0, choices=MEDIA_TYPE, verbose_name=u'媒体类型')

    media_id = models.CharField(
        blank=False, max_length=64, verbose_name=u'媒体ID')

    picurl = models.CharField(
        blank=True, null=True, max_length=200, verbose_name=u'图片地址')

    vformat = models.CharField(
        blank=True, null=True, max_length=5, verbose_name=u'音频格式')

    thumbmediaid = models.CharField(
        blank=True, null=True, max_length=64, verbose_name=u'缩略图媒体ID')

    confirmed = models.BooleanField(default=False, verbose_name=u'是否确认')

    url = models.CharField(max_length=100, default='', verbose_name=u'存储地址')

    def __unicode__(self):
        return self.relate_to

    class Meta:
        verbose_name = '二维码媒体项'
        verbose_name_plural = '二维码媒体项'

    def ext_name(self):
        if self.media_type == 1:
            return self.vformat
        elif self.media_type == 2:
            return 'jpg'
        elif self.media_type == 3:
            return 'mp4'
        return ''
