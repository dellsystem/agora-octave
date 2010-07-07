from django.conf.urls.defaults import *

urlpatterns = patterns('agora.apps.free_license.views',
    (r'^$', 'index'),
    (r'^(?P<license_name>\w*)/$', 'show_license'),
)
