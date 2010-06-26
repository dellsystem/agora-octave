from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^$',
     'django.views.generic.simple.direct_to_template',
     {'template': 'index.djhtml'}),


    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^', include('agora.apps.bundle.urls'))

)

#Let Django itself serve static data during debugging
from django.conf import settings

if settings.DEBUG:
     urlpatterns += patterns('',
                    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                    {'document_root': 'static/', 'show_indexes': True}),
                    )

