from django.conf.urls.defaults import *

urlpatterns = patterns('agora.apps.profile.views',
    url(r'^editprofile$', 'editprofile', name='edit_profile'),
    url(r'^(?P<username>\w*)/$', 'showprofile', name='show_profile'),
)
