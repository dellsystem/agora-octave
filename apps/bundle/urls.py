from django.conf.urls.defaults import *

urlpatterns = patterns('agora.apps.bundle.views',
    (r'^(?P<user>.*)/(?P<bundle>.*)/$', 'detail'),
    (r'^$', 'index'),
)

