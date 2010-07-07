from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from agora.apps.free_license.models import FreeLicense
from agora.apps.bundle.models import Bundle
from agora.apps.snippet.models import Snippet
from agora.apps.profile.models import Profile

from agora.middleware.http import Http403

def getprofile(user):
    u = get_object_or_404(User, username=user)

    #Inactive users "don't exist"
    if not u.is_active:
        raise Http404

    #Get profile or create a default if none exists
    try:
        p = u.get_profile()
    except Profile.DoesNotExist:
        #At least one FreeLicense *must* exist.
        p = Profile(user=u, preferred_license=FreeLicense.objects.get(id=1))
        p.save()

    return [u,p]

def showprofile(request, user):
    [u,p] = getprofile(user)

    if u.first_name or u.last_name:
        n = u.get_full_name()
    else:
        n = u.username

    b = Bundle.objects.filter(uploader=u)
    s = Snippet.objects.filter(uploader=u)

    return direct_to_template(request, 'profile/user.djhtml',
                              {
                                  'profile' : p,
                                  'bundles' : b,
                                  'snippets' : s,
                                  'name' : n,
                               },
                              )

@login_required
def editprofile(request, user):
    [u,p] = getprofile(user)

    #Make sure user can only edit own profile
    if request.user != u:
        raise Http403

    if request.method=='POST':
        u.first_name = request.POST['first-name']
        u.last_name  = request.POST['last-name']
        u.save()

        try:
            p.preferred_license = \
                            FreeLicense.objects.get(id=request.POST['license'])
        except:
            p.preferred_license = FreeLicense.objects.get(id=1)

        p.interests = request.POST['interests']
        p.blurb = request.POST['blurb']
        p.save()
        return HttpResponseRedirect(reverse(
                                    'agora.apps.profile.views.showprofile',
                                    args=(u,))
                                    )

    licenses = FreeLicense.objects.all()
    return direct_to_template(request, 'profile/edit-user.djhtml',
                              {
                                  'profile' : p,
                                  'licenses' : licenses,
                              },
                              )
