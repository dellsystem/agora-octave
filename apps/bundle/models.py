from django.db import models
from django.contrib.auth.models import User
from agora.apps.free_license.models import FreeLicense
from agora.apps.snippet.models import CodeLanguage

class Bundle(models.Model):
    name = models.CharField(max_length=256)
    uploader = models.ForeignKey(User)
    description = models.TextField(max_length=32728)
    free_license = models.ForeignKey(FreeLicense)
    pub_date = models.DateTimeField('date uploaded')
    mod_date = models.DateTimeField('date last modified')

    class Meta:
        #Every user must pick unique names for their bundles
        unique_together = ('uploader','name')

    def __unicode__(self):
        return self.name

class BundleFile(models.Model):
    name = models.CharField(max_length=256)
    bundle = models.ForeignKey(Bundle)
    bundle_file = models.FileField(upload_to='bundles/')
    def __unicode__(self):
        return self.name

class CodeFile(BundleFile):
    code = models.TextField()
    language = models.ForeignKey(CodeLanguage)
