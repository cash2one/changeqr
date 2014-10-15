#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 23:43:23
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-15 00:02:03

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from optparse import make_option
import os

from qrcode.models import Qrprefix, Qrcode


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('-p',dest='prefix_num',type='int',help='number of prefix'),
            make_option('-c',dest='code_num',type='int',help='number of code for each prefix'),
            make_option('-P',dest='prefix',type='string',help='prefix code'),
        )
    
    def handle(self, *args, **options):
        if options['prefix_num'] and options['code_num']:
            prefix_num = options['prefix_num']
            code_num = options['code_num']
            for p in xrange(prefix_num):
                prefix = Qrprefix.create()
                for c in xrange(code_num):
                    code = Qrcode.create(prefix.code)
                    print code.full

        elif options['prefix'] and options['code_num']:
            code_num = options['code_num']
            try:
                prefix = Qrprefix.objects.get(code=options['prefix'])
            except:
                prefix = Qrprefix.create(options['prefix'])
            for c in xrange(code_num):
                code = Qrcode.create(prefix.code)
                print code.full
            
