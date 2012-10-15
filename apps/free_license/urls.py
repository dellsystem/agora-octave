from django.conf.urls.defaults import *

urlpatterns = patterns('apps.free_license.views',
    url(r'^$', 'index', name='license_info'),
    (r'^(?P<license_name>\w*)/$', 'show_license'),
)
