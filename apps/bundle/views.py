from django.shortcuts import render_to_response, get_object_or_404
from agora.apps.bundle.models import *

def detail(request, user, bundle):
    b = get_object_or_404(Bundle, uploader__username=user, name=bundle)
    f = BundleFile.objects.filter(bundle=b)

    return render_to_response('bundle/index.djhtml', {'bundle':b,
                                                      'files': f,})
