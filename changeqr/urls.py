from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'changeqr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    url(r'^gateway/$', 'qrcode.views.weixin.gateway', name='gateway'),
)

urlpatterns += patterns('web.views',
	url(r'^web/', include('web.urls')),
)