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

    def handle(self, *args, **options):
        prefix_count = int(args[0])
        count = int(args[1])

        for p in xrange(prefix_count):
            prefix = Qrprefix.create()
            for c in xrange(count):
                code = Qrcode.create(prefix.code)
                print code.full
