from django.db import models
from django.contrib.auth.models import User

from agora.apps.free_license.models import FreeLicense
from agora.apps.pygments_style.models import PygmentsStyle


class Profile(models.Model):
    user = models.OneToOneField(User)
    preferred_license = models.ForeignKey(FreeLicense, default=1)
    interests = models.CharField(max_length=512, null=True, blank=True)
    blurb = models.TextField(max_length=16384, null=True, blank=True)
    pygments_style = models.ForeignKey(PygmentsStyle, default=1)

    def __unicode__(self):
        return self.user.username


# Defines a post_save hook to ensure that a profile is created for each user
# This also ensures that the admin user (created when running syncdb) has one
def create_user_profile(sender, instance, created, **kwards):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
