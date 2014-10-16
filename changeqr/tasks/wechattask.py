#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-10-10 21:58:26
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-16 14:16:43

import logging
import uuid
import os
from datetime import datetime
import subprocess

from django_rq import job
from django.conf import settings

from qrcode.models import CodeContent
from changeqr.wechat.wechat import Wechat


logger = logging.getLogger('tasks')

CONVERT_CMD = 'ffmpeg -i %s -b 8k -ar 44100 %s'


def voice_transcode(src, dest):
    '''
    从 amr 格式转化为 mp3 格式
    '''
    subprocess.Popen(CONVERT_CMD % (src, dest), shell=True)


@job
def download_media(content_id):
    logger.info('task start %s ' % content_id)

    weixinapi = settings.WEIXIN_API
    appid = weixinapi['APP_ID']
    appsecret = weixinapi['APP_SECRET']
    token = weixinapi['TOKEN']

    content = CodeContent.objects.get(pk=content_id)

    if content.status != 2:
        raise Exception('Content Status error! %s' % content_id)

    medias = content.codemedia_set.all()

    wechat = Wechat(token=token, appid=appid, appsecret=appsecret)

    for media in medias:
        logger.info(media.media_id)
        now = datetime.now()
        logger.info(media.get_media_type_display())

        subpath = os.path.join(
            media.get_media_type_display(), str(now.year), str(now.month))
        path = os.path.join(settings.MEDIA_ROOT, subpath)

        if not os.path.exists(path):
            os.makedirs(path)

        fprefix = uuid.uuid1()
        fext = media.ext_name()
        fname = '%s.%s' % (fprefix, fext)

        full = os.path.join(path, fname)

        try:
            ret = wechat.download_media(media.media_id)
            with open(full, 'w') as fp:
                fp.write(ret.content)

            logger.info('File saved to %s' % full)

            if fext == 'amr':
                fnew = '%s.mp3' % fprefix
                full_new = os.path.join(path, fnew)
                voice_transcode(full, full_new)
                fname = fnew

            media.url = os.path.join(subpath, fname)

            media.save()

        except Exception, e:
            import traceback
            logger.error(traceback.print_exc())
            raise Exception(
                'Download media failed! content_id = %s, media_id = %s, Exception: %s' %
                (content_id, media.media_id, e))

    # 状态标注为媒体已下载
    content.status = 3
    content.save()

    logger.info('task end %s ' % content_id)
