#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 22:54:32
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-14 23:05:13

from django.contrib import admin


class QrprefixAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('title', 'code')
    search_fields = ('title', 'code')
    list_per_page = 20


class QrcodeAdmin(admin.ModelAdmin):
    list_filter = ('ctype', 'status',)
    list_display = ('full', 'status', 'visit_count',)
    search_fields = ('prefix', )
    list_per_page = 20


class SubcodeAdmin(admin.ModelAdmin):
    list_filter = ('qrcode', )
    list_display = ('qrcode', 'postfix', 'full', 'visit_count', )
    search_fields = ('qrcode', )
    list_per_page = 20


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
