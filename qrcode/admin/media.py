#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 22:56:50
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-14 23:18:24

from django.contrib import admin


class CodeContentAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_display = (
        'qrcode', 'status', 'uid', 'text', 'image_count', 'voice_count', )
    search_fields = ('qrcode', 'uid', )
    list_per_page = 20


class CodeMediaAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('relate_to', 'media_type', 'media_id')
    search_fields = ('title', 'code')
    list_per_page = 20
