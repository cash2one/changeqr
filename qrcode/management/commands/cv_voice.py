#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-10-16 12:57:51
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-16 14:04:37

# Convert voice format to mp3

from optparse import make_option
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from qrcode.models import CodeMedia, CodeContent
from changeqr.tasks.wechattask import voice_transcode


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-m', '--media', dest='media', type='int', help='media id'),
        make_option('-a', '--all', dest='all', action='store_true')
    )

    def handle(self, *args, **options):
        if options['media']:
            media_id = options['media']
            media = CodeMedia.objects.filter(pk=media_id).first()
            if not media:
                print 'media not found %s ' % media_id
                return

            if media.url and media.url[-3:] == 'amr':
                self.convert_media(media)

        elif options['all']:
            medias = CodeMedia.objects.filter(media_type=1)
            for media in medias:
                if media.url and media.url[-3:] == 'amr':
                    self.convert_media(media)

    def convert_media(self, media):
        nurl = '%smp3' % media.url[:-3]
        path = os.path.join(settings.MEDIA_ROOT, media.url)
        npath = '%smp3' % path[:-3]

        voice_transcode(path, npath)

        media.url = nurl
        media.save()
