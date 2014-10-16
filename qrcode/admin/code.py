#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 22:54:32
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-16 16:09:23

from django.contrib import admin

from datetime import datetime


def code_active(self, request, queryset):
    '''
    激活新创建的二维码
    '''
    queryset.filter(status=0).update(status=1, active_at=datetime.now())


def code_frozen(self, request, queryset):
    '''
    冻结正在使用的二维码
    '''
    queryset.filter(status=2).update(status=3)

code_active.short_description = u'激活选中的 二维码'
code_frozen.short_description = u'冻结选中的 二维码'


class QrprefixAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('title', 'code')
    search_fields = ('title', 'code')
    list_per_page = 20


class QrcodeAdmin(admin.ModelAdmin):
    list_filter = ('ctype', 'status',)
    list_display = ('full', 'prefix', 'status', 'visit_count',)
    search_fields = ('prefix', )
    list_per_page = 50

    actions = [code_active, code_frozen]


class SubcodeAdmin(admin.ModelAdmin):
    list_filter = ('qrcode', )
    list_display = ('qrcode', 'postfix', 'full', 'visit_count', )
    search_fields = ('qrcode', )
    list_per_page = 50


# class CustomerProfileInline(admin.TabularInline):
#     model = CustomerProfile


# class CustomerAdmin(admin.ModelAdmin):
#     list_filter = ()
#     list_display = ('user', 'nickname',
#                     'openid', 'access_token', 'expires_at', )
#     search_fields = ('nickname',)
#     list_per_page = 20

#     inlines = [
#         CustomerProfileInline
#     ]
