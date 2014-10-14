from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'changeqr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin20144102/', include(admin.site.urls)),

    url(r'^djangorq20144102/', include('django_rq.urls')),

    url(r'^gateway/$', 'qrcode.views.weixin.gateway', name='gateway'),
    url(r'^queue/(?P<id>\d*)/$', 'qrcode.views.weixin.enqueue', name='enqueue'),
    url(r'^menu/20141012/$', 'qrcode.views.weixin.menu'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
)

urlpatterns += patterns('web.views',
    url(r'^$', 'index', name='index'),
    url(r'^wap/(?P<code>[a-zA-Z0-9]{20})$', 'wap_media', name='media'),
)