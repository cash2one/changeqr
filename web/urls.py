from django.conf.urls import patterns, url

urlpatterns = patterns('web.views',
	url(r'^$', 'index', name='index'),
	url(r'^wap_media/$', 'wap_media', name='media'),
)