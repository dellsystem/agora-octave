from django import forms

from apps.bundle.models import Bundle


class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ('uploader', 'name', 'description', 'octave_format',
            'free_license')
        widgets = {
            # Ideally, the uploader field should just not show up at all
            # Not really possible if we want to validate the name
            # This is the next best option (hidden fields just aren't shown)
            'uploader': forms.HiddenInput,
        }

    file = forms.FileField(help_text=("Upload a plain text file or an \
        archive file."))

    def clean(self):
        data = self.cleaned_data
        name_used = Bundle.objects.filter(uploader=data.get('uploader'),
            name=data.get('name')).exists()

        # If a bundle with this user/name combo exists, raise an error
        if name_used:
            raise forms.ValidationError("You have already created a bundle"
                " with this name.")

        return data


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
