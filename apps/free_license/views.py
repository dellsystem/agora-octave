from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from apps.free_license.models import FreeLicense

def index(request,  licenses = FreeLicense.objects.all() ):
    return direct_to_template(request, 'licenses/index.djhtml',
                              {'licenses' : licenses},
                              )

def show_license(request, license_name, licenses = FreeLicense.objects.all()):

    lic = get_object_or_404(FreeLicense, name=license_name)

    return direct_to_template(request, 'licenses/license.djhtml',
                              {'license' : lic,
                               'licenses' : licenses},
                              )
