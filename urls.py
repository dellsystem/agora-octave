from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^$',
     'django.views.generic.simple.direct_to_template',
     {'template': 'index.html'}),
    # Example:
    # (r'^agora/', include('agora.foo.urls')),

    #(r'^mippets/$', 'agora.mippet.views.index'),
   
    #(r'^mippets/(?P<name>.*)/$', 'agora.mippet.views.detail'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)
