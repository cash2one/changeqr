#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-15 15:00:55
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-15 16:30:53

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from qrcode.models import CodeMedia, CodeContent
from changeqr.wechat.wechat import Wechat

from optparse import make_option
from datetime import datetime
import os
import uuid


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-m', '--media', dest='media', type='int', help='media id'),
        make_option(
            '-c', '--content', dest='content', type='int', help='content id'),
        make_option('-a', '--all', dest='all', action='store_true')
    )

    def handle(self, *args, **options):

        weixinapi = settings.WEIXIN_API
        wechat = Wechat(token=weixinapi['TOKEN'], appid=weixinapi[
                        'APP_ID'], appsecret=weixinapi['APP_SECRET'])

        if options['media']:
            media_id = options['media']
            media = CodeMedia.objects.filter(pk=media_id).first()
            if not media:
                print 'CodeMedia %d does not exist!' % media_id
                return

            self.dl_media(wechat, media)
        elif options['content']:
            content_id = options['content']
            content = CodeContent.objects.filter(pk=content_id).first()
            if not content:
                print 'CodeContent %d does not exist!' % content_id
                return
            self.dl_content(wechat, content)
        elif options['all']:
            contents = CodeContent.objects.filter(status=2)[:10]
            for content in contents:
                self.dl_content(wechat, content)

    def dl_content(self, wechat, content):
        medias = content.codemedia_set.all()
        for media in medias:
            self.dl_media(wechat, media)

        content.status = 3
        content.save()

    def dl_media(self, wechat, media):
        now = datetime.now()
        print media.get_media_type_display()

        subpath = os.path.join(
            media.get_media_type_display(), str(now.year), str(now.month))
        path = os.path.join(settings.MEDIA_ROOT, subpath)

        if not os.path.exists(path):
            os.makedirs(path)

        fname = '%s.%s' % (uuid.uuid1(), media.ext_name())
        full = os.path.join(path, fname)

        try:
            ret = wechat.download_media(media.media_id)
            with open(full, 'w') as fp:
                fp.write(ret.content)

            print 'File saved to %s' % full

            media.url = os.path.join(subpath, fname)

            media.save()

        except Exception, e:
            raise Exception(
                'Download media failed! content_id = %s, media_id = %s, Exception: %s' %
                (content_id, media.media_id, e))
