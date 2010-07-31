from django.conf.urls.defaults import patterns, url
from django.conf import settings

urlpatterns = patterns('agora.apps.snippet.views',
    url(r'^$',
        'snippet_new', name='snippet_new'),
                       
    url(r'^guess/$',
        'guess_lexer', name='snippet_guess_lexer'),
                       
    url(r'^diff/$',
        'snippet_diff', name='snippet_diff'),

    url(r'^your-latest/$',
        'snippet_userlist', name='snippet_userlist'),
                       
    url(r'^your-settings/$',
        'userprefs', name='snippet_userprefs'),
                       
    url(r'^(?P<snippet_id>[a-zA-Z0-9]{4})/$',
        'snippet_details', name='snippet_details'),
                       
    url(r'^(?P<snippet_id>[a-zA-Z0-9]{4})/delete/$',
        'snippet_delete', name='snippet_delete'),

    url(r'^(?P<snippet_id>[a-zA-Z0-9]{4})/raw/$',
        'snippet_details',
          {'template_name': 'snippet/snippet_details_raw.djhtml',
           'is_raw': True},
        name='snippet_details_raw'),
)
