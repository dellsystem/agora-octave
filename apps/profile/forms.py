from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.profile.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # Change the help text for names
        name_text = _("We will display your name according to most Western \
        European conventions, your given name(s) followed by your surname(s).")
        self.fields['first_name'].help_text = name_text
