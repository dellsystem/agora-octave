from django.shortcuts import get_object_or_404
from agora.apps.bundle.models import *
from django.views.generic.simple import direct_to_template

def detail(request, user, bundle):
    b = get_object_or_404(Bundle, uploader__username=user, name=bundle)
    f = BundleFile.objects.filter(bundle=b)

    return direct_to_template(request, 'bundle/index.djhtml',
                              {
                                'bundle':b,
                                'files': f,
                               },
                              )
