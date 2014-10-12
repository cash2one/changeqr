#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-09 10:59:35
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-12 14:20:45

# 需要在 __init__.py 中执行 from qrhandler import *， 否则handler无法被注册

from changeqr.wechat.handler import BaseHandler, handler

from qrcode.models import Qrcode, CodeContent, CodeMedia
from messages import L10N_MESSAGES as MSG

import re
import logging
from datetime import datetime

logger = logging.getLogger('qrcode')


def handle_qrcode(code, message):
    '''
    处理已经识别的二维码字符串
    '''

    old = CodeContent.objects.filter(uid=message.fromuser, status=1).first()
    if old:
        return message.wechat.reply_text(MSG['busy'])

    qrcode = Qrcode.objects.filter(full=code).first()
    if not qrcode:
        return message.wechat.reply_text(MSG['unauthorized'])

    if qrcode.status == 2:
        return message.wechat.reply_text(MSG['used'])
    elif qrcode.status != 1:
        return message.wechat.reply_text(MSG['inactive'])

    # 新建媒体内容
    content = CodeContent()

    content.qrcode = qrcode
    content.uid = message.fromuser
    content.status = 1  # interactive
    content.save()

    qrcode.status = 4  # editing
    qrcode.save()

    return message.wechat.reply_text(MSG['welcome'])


def print_menu(message):
    '''
    打印菜单
    '''

    return message.wechat.reply_text(MSG['menu'])


def save_interactive(message, content):
    '''
    保存上一步的媒体内容
    '''
    media = CodeMedia.objects.filter(
        relate_to=content, confirmed=False).first()
    if media:
        media.confirmed = True
        media.save()

def print_inactive(message, content, media=''):
    '''
    打印交互信息
    '''
    to_print = []
    if not content.text:
        to_print.append(MSG['step_text'])
    if content.image_count < 6:
        to_print.append(MSG['step_img'] % (6 - content.image_count))
    if content.voice_count < 1:
        to_print.append(MSG['step_voice'])

    if len(to_print) > 0:
        return message.wechat.reply_text(MSG['step'] % (media, ','.join(to_print)))
    else:
        return message.wechat.reply_text(MSG['step_nomore'] % media)


@handler.register('event')
class QrcodeHandler(BaseHandler):

    _pattern = re.compile(r'^([a-zA-Z0-9]{4}-[a-zA-Z0-9]{15})$')

    def handle(self, message):
        if not message.event == 'scancode_waitmsg':
            return

        match = self._pattern.match(message.scanresult)

        if match:
            return handle_qrcode(match.group(1), message)


@handler.register('text')
class TextQrcodeHandler(BaseHandler):

    '''
    用户在公众账号中直接输入二维码内容
    media_type = 0
    '''

    _pattern = re.compile(r'^([a-zA-Z0-9]{4}-[a-zA-Z0-9]{15})$')

    def handle(self, message):
        match = self._pattern.match(message.content)

        if match:
            return handle_qrcode(match.group(1), message)

        if message.content == '0':
            # 重传图片
            content = CodeContent.objects.filter(
                uid=message.fromuser, status=1).first()
            if not content:
                return

            if content.last_media is not None:
                if content.last_media == 0:
                    content.text = ''
                    content.last_media = None
                    content.save()
                else:
                    media = content.codemedia_set.filter(confirmed=False).first()
                    if media:
                        media.delete()

                    content.decr(media.media_type)

            return message.wechat.reply_text(MSG['rollback'])
        elif message.content == '1':
            # 完成上传
            content = CodeContent.objects.filter(
                uid=message.fromuser, status=1).first()
            save_interactive(message, content)

            content.status = 2
            content.last_media = None
            content.save()

            content.qrcode.status = 2
            content.used_at = datetime.now()
            content.qrcode.save()

            # 推送消息到消息队列，完成图片、音频、视频下载
            from changeqr.tasks.wechattask import download_media
            download_media.delay(content.pk)

            return message.wechat.reply_text(MSG['success'])
        elif message.content == '9':
            content = CodeContent.objects.filter(
                uid=message.fromuser, status=1).first()
            if not content:
                return

            for media in content.codemedia_set.all():
                media.delete()
                media.save()

            content.text = ''
            content.image_count = 0
            content.video_count = 0
            content.voice_count = 0
            content.last_media = None

            content.save()

            return message.wechat.reply_text(MSG['welcome'])
        elif message.content == '?':
            return print_menu(message)
        else:
            content = CodeContent.objects.filter(
                uid=message.fromuser, status=1).first()
            save_interactive(message, content)

            if len(message.content) > 200:
                return message.wechat.reply_text(MSG['texttoolong'])

            if not content.accept_more(0):
                return message.wechat.reply_text(MSG['textalreadyset'])
            # 输入文字内容
            content.text = message.content
            content.last_media = 0
            content.save()

            return print_inactive(message, content, media='文字')


@handler.register('image')
class ImageHandler(BaseHandler):

    '''
    图片消息处理 
    media_type = 2
    '''

    def handle(self, message):
        content = CodeContent.objects.filter(
            uid=message.fromuser, status=1).first()
        if not content:
            return print_menu(message)

        if not content.accept_more(2):
            return message.wechat.reply_text(MSG['imagealreadyset'])

        save_interactive(message, content)

        media = CodeMedia.objects.create(relate_to=content)
        media.media_type = 2
        media.media_id = message.mediaid

        media.picurl = message.picurl

        media.confirmed = False

        media.save()

        content.incr(media.media_type)

        return print_inactive(message, content, media='照片')


@handler.register('voice')
class VoiceHandler(BaseHandler):

    '''
    音频消息处理
    media_type = 1
    '''

    def handle(self, message):

        content = CodeContent.objects.filter(
            uid=message.fromuser, status=1).first()
        if not content:
            return print_menu(message)

        if not content.accept_more(1):
            return message.wechat.reply_text(MSG['voicealreadyset'])

        save_interactive(message, content)

        media = CodeMedia.objects.create(relate_to=content)
        media.media_type = 1
        media.media_id = message.mediaid

        media.vformat = message.format

        media.confirmed = False

        media.save()

        content.incr(media.media_type)

        return print_inactive(message, content, media='语音')


# 暂时不对视频进行处理
# @handler.register('video')
class VideoHandler(BaseHandler):

    '''
    视频消息处理
    media_type = 3
    '''

    def handle(self, message):

        content = CodeContent.objects.filter(
            uid=message.fromuser, status=1).first()
        if not content:
            return print_menu(message)

        save_interactive(message, content)

        media = CodeMedia.objects.create(relate_to=content)
        media.media_type = 3
        media.media_id = message.mediaid

        media.thumbmediaid = message.thumbmediaid

        media.confirmed = False

        media.save()

        content.incr(media.media_type)

        return print_inactive(message, content, media='视频')


@handler.register('event')
class SubscribeHandler(BaseHandler):
    '''
    关注公众号事件响应
    点击帮助事件
    '''
    def handle(self, message):
        if message.event == 'subscribe':
            return message.wechat.reply_text(MSG['menu'])

        if message.event == 'click' and message.eventkey == 'help':
            return message.wechat.reply_text(MSG['menu'])



@handler.register('video', level=1)
@handler.register('text', level=1)
@handler.register('image', level=1)
@handler.register('voice', level=1)
@handler.register('event', level=1)
class LoggerHandler(BaseHandler):

    def handle(self, message):
        logger.info(message.raw)
