from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    code = models.TextField(max_length=32768)
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    uploader = models.ForeignKey(User)
    pub_date = models.DateTimeField('date uploaded')
    mod_date = models.DateTimeField('date last modified')

    def __unicode__(self):
        if self.name:
            return self.name
        return self.id

class CodeLanguage(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return name
