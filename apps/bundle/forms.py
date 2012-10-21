from django import forms

from apps.bundle.models import Bundle


class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ('name', 'description', 'free_license')

    file = forms.FileField(help_text=("Upload a plain text file or an \
        archive file."))


class BundleEditForm(forms.ModelForm):
    """
    Like BundleForm, but for editing bundles. A new form is needed because
    the name field should not be editable after creation, and because the
    file field shouldn't be required in this case
    """
    class Meta:
        model = Bundle
        fields = ('description', 'free_license')

    file = forms.FileField(help_text=("Upload a plain text file or an \
        archive file to update the version."), required=False)
