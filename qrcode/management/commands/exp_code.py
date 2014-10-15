#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 23:43:23
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-15 00:02:03

from django.core.management.base import BaseCommand
from optparse import make_option
import os

from qrcode.models import Qrprefix, Qrcode
from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('-o',dest='path',type='string',help='output file to save'),
            make_option('-a',dest='all',action='store_true',help='export all code of status 0'),
            make_option('-p',dest='prefix',type='string',help='export code of prefix code with status 0'),
        )
    
    def handle(self, *args, **options):
        if options['path'] and options['all']:
            codes = Qrcode.objects.filter(status=0)
            with open(options['path'],'w') as f:
                for code in codes:
                    f.write('%s%s\n' %(settings.API_URL,code.full))
        elif options['path'] and options['prefix']:
            codes = Qrcode.objects.filter(status=0, prefix=options['prefix'])
            with open(options['path'],'w') as f:
                for code in codes:
                    f.write('%s%s\n' %(settings.API_URL,code.full))
            
