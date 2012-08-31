from django.db import models
from django.contrib.auth.models import User

from agora.apps.free_license.models import FreeLicense


class Profile(models.Model):
    user = models.OneToOneField(User)
    preferred_license = models.ForeignKey(FreeLicense)
    interests = models.CharField(max_length=512)
    blurb = models.TextField(max_length=16384)

    def __unicode__(self):
        return self.user.username
