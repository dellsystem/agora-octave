from django.conf.urls.defaults import *
from django.views.generic import ListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'index.djhtml'},
        name='home'),
    url(r'^about$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'about.djhtml'},
        name='about'),
    url(r'^help$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'help.djhtml'},
        name='help'),
    url(r'^discuss$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'discuss.djhtml'},
        name='discuss'),
    url(r'^code$',
        'views.code',
        name='code'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout',
        {'template_name' : 'index.djhtml', 'next_page' : '/'}),
    url(r'^accounts/', include('registration.urls')),
    url(r'^licenses/', include('agora.apps.free_license.urls')),
    url(r'^users/', include('agora.apps.profile.urls')),
    url(r'^snippet/', include('agora.apps.snippet.urls')),
    url(r'^bundles/', include('agora.apps.bundle.urls')),
)

#Let Django itself serve static data during debugging
from django.conf import settings

if settings.DEBUG:
     urlpatterns += patterns('',
                    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                    {'document_root': 'static/', 'show_indexes': True}),
                    )

