from django.template import Context, loader
from django.http import HttpResponse
from agora.apps.bundle.models import *

def detail(request, user, bundle):
    t = loader.get_template('bundle/index.djhtml')
    c = Context({
        'user': user,
        'bundle' : bundle,
    })
    return HttpResponse(t.render(c))
