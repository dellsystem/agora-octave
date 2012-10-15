from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.free_license.models import FreeLicense
from apps.pygments_style.models import PygmentsStyle


class Profile(models.Model):
    user = models.OneToOneField(User)
    preferred_license = models.ForeignKey(FreeLicense, help_text=_("\
        By default, all of your submissions will be under the following \
        license, and this license will be displayed next to your \
        submissions. <a href=\"/licenses/\">Find out more.</a>"),
        default=1)
    interests = models.CharField(max_length=512, null=True, help_text=_("\
        Tell us about your research interests (e.g. \
        <em>signal processing</em>, <em>hyperbolic PDEs</em>). These \
        keywords will be used when searching for submissions."), blank=True,
        verbose_name=_("Research interests"))
    blurb = models.TextField(max_length=16384, null=True, help_text=_("\
        Finally, anything else you would like to say about yourself."),
        blank=True)
    pygments_style = models.ForeignKey(PygmentsStyle, default=1,
        verbose_name=_('Syntax highlighting style'), help_text=_("\
        Choose a stylesheet for displayed syntax-highlighted code. Most of \
        these stylesheets are based off of default Pygments stylesheets."))

    def __unicode__(self):
        return self.user.username


# Defines a post_save hook to ensure that a profile is created for each user
# This also ensures that the admin user (created when running syncdb) has one
def create_user_profile(sender, instance, created, **kwards):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
