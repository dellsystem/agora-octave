import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from pygments import lexers, highlight, formatters, util
from mptt.models import MPTTModel, TreeForeignKey
from sizefield.models import FileSizeField

from apps.free_license.models import FreeLicense
from apps.snippet.highlight import NakedHtmlFormatter


class Bundle(models.Model):
    class Meta:
        # Every user must pick unique names for their bundles
        unique_together = ('uploader','name')
        ordering = ['-pub_date']

    name = models.SlugField(help_text=_("Your bundle will be accessible " +
        "from a URL that uses the name you enter here, so choose wisely. " +
        "Acceptable characters: alphanumeric characters, hyphens, and " +
        "underscores."))
    uploader = models.ForeignKey(User)
    description = models.TextField(max_length=32728)
    free_license = models.ForeignKey(FreeLicense, default=1)
    pub_date = models.DateTimeField('date uploaded', auto_now_add=True)
    mod_date = models.DateTimeField('date last modified', auto_now=True)
    done_uploading = models.BooleanField(default=False)
    file_name = models.CharField(max_length=256) # the uploaded file

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('bundle_details', [self.uploader.username, self.name])

    def get_temp_path(self):
        return os.path.join('tmp', 'bundles', '%s' % self.id)


class BundleFile(MPTTModel):
    bundle = models.ForeignKey(Bundle)
    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')
    name = models.CharField(max_length=256)
    is_dir = models.BooleanField()
    code = models.TextField(null=True, blank=True)
    full_path = models.CharField(max_length=256)
    file_size = FileSizeField(default=0) # for directories

    def __unicode__(self):
        return self.name

    def get_path(self):
        if self.parent:
            return os.path.join(self.parent.get_path(), self.name)
        else:
            return self.name

    def get_lines(self):
        return self.code.splitlines()

    def save_file_contents(self, file, original_filename=None):
        code = file.read()

        if original_filename is not None:
            filename = original_filename
        else:
            filename = file.name

        try:
            lexer = lexers.get_lexer_for_filename(filename)
            print "lexer is:"
            print lexer
        except util.ClassNotFound:
            print "can't guess the lexer"
            lexer = lexers.TextLexer()

        self.code = highlight(code, lexer, NakedHtmlFormatter())
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('bundlefile_details', [
            self.bundle.uploader.username,
            self.bundle.name,
            self.get_path()
        ])
