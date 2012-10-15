from django import forms

from apps.bundle.models import Bundle


class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ('uploader', 'name', 'description', 'free_license')

    file = forms.FileField(help_text=("Upload a plain text file or an \
        archive file."))
