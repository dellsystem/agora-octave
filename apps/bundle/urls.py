from django.conf.urls.defaults import *


BUNDLE_PATTERN = r'^(?P<user>[^/]*)/(?P<bundle>[^/]+)'
VERSION_PATTERN = '(?P<version>\d+)'


urlpatterns = patterns('apps.bundle.views',
    url(BUNDLE_PATTERN + '/?$', 'detail', name='bundle_details'),
    url(BUNDLE_PATTERN + '/' + VERSION_PATTERN + '/?$', 'detail',
        name='bundle_version'),
    url(BUNDLE_PATTERN + '/edit', 'edit', name='bundle_edit'),
    url(BUNDLE_PATTERN + '/' + VERSION_PATTERN + '/(?P<path>.+)/?$',
        'file_detail', name='bundlefile_details'),
    url(r'^$', 'index', name='bundle_new'),
    url(r'^explore$', 'explore', name='bundle_explore'),
)
