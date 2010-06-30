from django.shortcuts import render_to_response, get_object_or_404
from agora.apps.profile.models import Profile
from django.contrib.auth.models import User
from django.http import Http404
from agora.apps.free_license.models import FreeLicense
from agora.apps.bundle.models import Bundle
from agora.apps.snippet.models import Snippet

def showprofile(request, user):
    u = get_object_or_404(User, username=user)

    #Inactive users "don't exist"
    if not u.is_active:
        raise Http404

    try:
        p = u.get_profile()
    #Create a default profile if none exists
    except Profile.DoesNotExist:
        #At least one FreeLicense *must* exist.
        p = Profile(user=u, preferred_license=FreeLicense.objects.get(id=1))
        p.save()

    b = Bundle.objects.filter(uploader=u)
    s = Snippet.objects.filter(uploader=u)

    return render_to_response('user.djhtml', {'user' : u,
                                              'profile' : p,
                                              'bundles' : b,
                                              'snippets' :s,
                                              })
