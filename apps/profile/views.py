from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.free_license.models import FreeLicense
from apps.bundle.models import Bundle
from apps.snippet.models import Snippet
from apps.profile.models import Profile
from apps.profile.forms import UserForm, ProfileForm


def showprofile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()

    if user.first_name or user.last_name:
        name = user.get_full_name()
    else:
        name = user.username

    b = Bundle.objects.filter(uploader=user)
    s = Snippet.objects.filter(author=user)

    context = {
        'profile': user.get_profile,
        'name': name,
        'bundles': Bundle.objects.filter(uploader=user),
        'snippets': Snippet.objects.filter(author=user),
    }

    return render(request, 'profile/user.djhtml', context)


@login_required
def editprofile(request):
    user = request.user
    profile = user.get_profile()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(user)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'profile/edit-user.djhtml', context)
