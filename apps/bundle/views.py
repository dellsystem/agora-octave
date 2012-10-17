from __future__ import with_statement

import os

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.bundle.models import Bundle, BundleFile
from apps.bundle.forms import BundleForm
from apps.bundle.tasks import handle_bundle_upload
from apps.pygments_style.models import PygmentsStyle


def detail(request, user, bundle, file=None):
    bundle = get_object_or_404(Bundle, uploader__username=user, name=bundle)
    files = bundle.bundlefile_set.all()

    if request.user.is_authenticated():
        pygments_style = request.user.get_profile().pygments_style
    else:
        pygments_style = PygmentsStyle.objects.get(pk=1)

    context = {
        'default_style': pygments_style,
        'pygments_styles': PygmentsStyle.objects.all(),
        'bundle': bundle,
        'files': files,
        'file': file,
    }

    return render(request, 'bundle/bundle.djhtml', context)


def file_detail(request, user, bundle, path):
    bundle_file = get_object_or_404(BundleFile, bundle__uploader__username=user,
        bundle__name=bundle, full_path=path, is_dir=False)

    return detail(request, user, bundle, file=bundle_file)

@login_required
def index(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['uploader'] = request.user.id
        form = BundleForm(post_data,
                          request.FILES)

        if form.is_valid():
            file = request.FILES.get('file')
            bundle = form.save()

            bundle.file_name = file.name
            bundle.save()
            bundle_path = bundle.get_temp_path()

            with open(bundle_path, 'wb+') as destination:
                for chunk in request.FILES.get('file', []):
                    destination.write(chunk)

            handle_bundle_upload.delay(bundle.id)

            return redirect(bundle)
    else:
        form = BundleForm()

    context = {
        'form': form,
        'bundles': Bundle.objects.order_by('-pub_date')[:5]
    }
    return render(request, 'bundle/index.djhtml', context)


def explore(request):
    context = {
        'recent_bundles': Bundle.objects.all()[:20]
    }

    return render(request, "snippet/explore.html", context)
