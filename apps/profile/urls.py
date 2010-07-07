from django.conf.urls.defaults import *

urlpatterns = patterns('agora.apps.profile.views',
    (r'^editprofile/(?P<user>\w*)/$', 'editprofile'),
    (r'^(?P<user>\w*)/$',             'showprofile'),
)
