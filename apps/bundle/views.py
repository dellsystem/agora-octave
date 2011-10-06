from django.shortcuts import get_object_or_404
from agora.apps.bundle.models import *
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse

def detail(request, user, bundle):
    b = get_object_or_404(Bundle, uploader__username=user, name=bundle)
    f = BundleFile.objects.filter(bundle=b)

    return direct_to_template(request, 'bundle/bundle.djhtml',
                              {
                                'bundle':b,
                                'files': f,
                               },
                              )

def index(request):
    try:
		b = Bundle.objects.all().order_by('pub_date')[:5]
    except Bundle.DoesNotExist:
        raise Http404

    return direct_to_template(request, 'bundle/index.djhtml',
                              {
                                'bundles':b,
                               },
                              )
