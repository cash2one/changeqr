from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'changeqr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^django-rq/', include('django_rq.urls')),

    url(r'^gateway/$', 'qrcode.views.weixin.gateway', name='gateway'),
    url(r'^test/$', 'qrcode.views.weixin.test', name='test'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
)

urlpatterns += patterns('web.views',
	url(r'^web/', include('web.urls')),
)