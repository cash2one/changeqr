#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-14 22:43:31
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-14 23:19:02

from django.contrib import admin


from qrcode.models import Qrprefix, Qrcode, Subcode, CodeContent, CodeMedia
from code import QrprefixAdmin, QrcodeAdmin, SubcodeAdmin
from media import CodeContentAdmin, CodeMediaAdmin

admin.site.register(Qrprefix, QrprefixAdmin)
admin.site.register(Subcode, SubcodeAdmin)
admin.site.register(Qrcode, QrcodeAdmin)

admin.site.register(CodeContent, CodeContentAdmin)
admin.site.register(CodeMedia, CodeMediaAdmin)
