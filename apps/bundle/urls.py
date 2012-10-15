from django.conf.urls.defaults import *


urlpatterns = patterns('apps.bundle.views',
    url(r'^(?P<user>[^/]+)/(?P<bundle>[^/]+)/(?P<path>.+)/$', 'file_detail',
        name='bundlefile_details'),
    url(r'^(?P<user>.*)/(?P<bundle>.*)/$', 'detail', name='bundle_details'),
    url(r'^$', 'index', name='bundle_new'),
    url(r'^explore$', 'explore', name='bundle_explore'),
)
