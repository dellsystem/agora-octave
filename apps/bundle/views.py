from __future__ import with_statement

import os

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.bundle.models import Bundle, BundleFile
from apps.bundle.forms import BundleForm, BundleEditForm
from apps.bundle.tasks import handle_bundle_upload
from apps.pygments_style.models import PygmentsStyle


def detail(request, user, bundle, file=None, version=0):
    bundle = get_object_or_404(Bundle, uploader__username=user, name=bundle)
    # If the version is not set, use the latest version
    version = int(version) or bundle.latest_version
    files = bundle.bundlefile_set.filter(version=version)

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
        'previous_versions': xrange(1, bundle.latest_version + 1),
        'this_version': version,
    }

    return render(request, 'bundle/bundle.djhtml', context)


def file_detail(request, user, bundle, version, path):
    print version
    bundle_file = get_object_or_404(BundleFile, bundle__uploader__username=user,
        bundle__name=bundle, full_path=path, is_dir=False, version=version)

    return detail(request, user, bundle, file=bundle_file, version=version)


@login_required
def index(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['uploader'] = request.user.id
        form = BundleForm(post_data, request.FILES)

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

    return render(request, "bundle/explore.djhtml", context)


@login_required
def edit(request, user, bundle):
    bundle = get_object_or_404(Bundle, name=bundle,
        uploader__username=request.user.username)

    # If the username specified in the URL is someone else's, show that page
    if user != request.user.username:
        # The bundle must exist, otherwise it would 404
        return redirect(bundle)

    if request.method == 'POST':
        form = BundleEditForm(request.POST, instance=bundle)

        if form.is_valid():
            form.save()

            file = request.FILES.get('file')
            if file is not None:
                bundle.done_uploading = False
                bundle.file_name = file.name
                bundle.latest_version += 1
                bundle.save()
                bundle_path = bundle.get_temp_path()

                with open(bundle_path, 'wb+') as destination:
                    for chunk in request.FILES.get('file', []):
                        destination.write(chunk)

                handle_bundle_upload.delay(bundle.id)
            return redirect(bundle)
    else:
        form = BundleEditForm(instance=bundle)

    context = {
        'bundle': bundle,
        'form': form,
    }

    return render(request, "bundle/edit.djhtml", context)
