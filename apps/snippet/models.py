from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    code = models.TextField(max_length=32768)
    uploader = models.ForeignKey(user)
    pub_date = models.DateTimeField('date uploaded')
    mod_date = models.DateTimeField('date last modified')
