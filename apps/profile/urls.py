from django.conf.urls.defaults import *

urlpatterns = patterns('apps.profile.views',
    url(r'^editprofile$', 'editprofile', name='edit_profile'),
    url(r'^(?P<username>\w*)/$', 'showprofile', name='show_profile'),
)
