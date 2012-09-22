from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from agora.apps.snippet.models import Snippet
from agora.apps.snippet.highlight import LEXER_LIST_ALL, LEXER_LIST, LEXER_DEFAULT
import datetime

#===============================================================================
# Snippet Form and Handling
#===============================================================================

EXPIRE_CHOICES = (
    (3600, _(u'In one hour')),
    (3600*24*7, _(u'In one week')),
    (3600*24*30, _(u'In one month')),
    (3600*24*30*12*100, _(u'Save forever')), # 100 years, I call it forever ;)
)

EXPIRE_DEFAULT = 3600*24*30

class SnippetForm(forms.ModelForm):
    file = forms.FileField(help_text=_("If the snippet you want to post is \
        saved as a file on your computer, you can upload it directly rather \
        than having to copy and paste it into the box above. If a file \
        is specified, the text in the content field above will be \
        ignored."),
        required=False)

    expire_options = forms.ChoiceField(
        choices=EXPIRE_CHOICES,
        initial=EXPIRE_DEFAULT,
        label=_(u'Expires'),
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(SnippetForm, self).__init__(*args, **kwargs)
        self.request = request

        try:
            if self.request.session['userprefs'].get('display_all_lexer',
                                                     False):
                self.fields['lexer'].choices = LEXER_LIST_ALL
        except KeyError:
            pass

        try:
            self.fields['author'].initial = \
                    self.request.session['userprefs'].get('default_name', '')
        except KeyError:
            pass

        # Make the content field not required (validated in clean())
        self.fields['content'].required = False
        self.fields['title'].required = True

    def clean(self):
        cleaned_data = super(SnippetForm, self).clean()
        file_data = cleaned_data.get('file')
        content = cleaned_data.get('content')

        if file_data:
            file_data.open()
            content_type = file_data.content_type

            # Do some very basic checking of types. NOT SECURE.
            if (content_type.startswith('text/') or
                content_type.startswith('application')):
                cleaned_data['content'] = file_data.read()
            else:
                raise forms.ValidationError(_("Please ensure that you upload \
                    a text file."))
        elif not content:
            # No snippet data specified
            raise forms.ValidationError(_("Please specify some content for \
                the snippet, either in the content field or by uploading \
                a file."))

        return cleaned_data

    def save(self, parent=None, *args, **kwargs):

        # Set parent snippet
        if parent:
            self.instance.parent = parent

        # Add expire datestamp
        self.instance.expires = datetime.datetime.now() + \
            datetime.timedelta(seconds=int(self.cleaned_data['expire_options']))

        # Save snippet in the db
        super(SnippetForm, self).save(*args, **kwargs)

        # Add the snippet to the user session list
        if self.request.session.get('snippet_list', False):
            if len(self.request.session['snippet_list']) >= \
                   getattr(settings, 'MAX_SNIPPETS_PER_USER', 10):
                self.request.session['snippet_list'].pop(0)
            self.request.session['snippet_list'] += [self.instance.pk]
        else:
            self.request.session['snippet_list'] = [self.instance.pk]

        return self.request, self.instance

    class Meta:
        model = Snippet
        fields = (
            'title',
            'content',
            'lexer',
        )


#===============================================================================
# User Settings
#===============================================================================

USERPREFS_FONT_CHOICES = [(None, _(u'Default'))] + [
    (i, i) for i in sorted((
        'Monaco',
        'Bitstream Vera Sans Mono',
        'Courier New',
        'Consolas',
    ))
]

USERPREFS_SIZES = [(None, _(u'Default'))] + [(i, '%dpx' % i) for i in range(5, 25)]

class UserSettingsForm(forms.Form):

    default_name = forms.CharField(label=_(u'Default Name'), required=False)
    display_all_lexer = forms.BooleanField(
        label=_(u'Display all lexer'),
        required=False,
        widget=forms.CheckboxInput,
        help_text=_(u'This also enables the super secret ' \
                     '\'guess lexer\' function.'),
    )
    font_family = forms.ChoiceField(label=_(u'Font Family'),
                                    required=False,
                                    choices=USERPREFS_FONT_CHOICES)
    font_size = forms.ChoiceField(label=_(u'Font Size'),
                                  required=False,
                                  choices=USERPREFS_SIZES)
    line_height = forms.ChoiceField(label=_(u'Line Height'),
                                    required=False,
                                    choices=USERPREFS_SIZES)
