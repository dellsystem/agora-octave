import datetime
import difflib
import random

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from agora.apps.snippet.highlight import LEXER_DEFAULT, LEXER_LIST, pygmentize
import agora.apps.mptt as mptt


t = 'abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890'
def generate_secret_id(length=4):
    return ''.join([random.choice(t) for i in range(length)])

class Snippet(models.Model):
    secret_id = models.CharField(_(u'Secret ID'), max_length=4, blank=True)
    title = models.CharField(_(u'Title'), max_length=120, blank=True)
    author = models.ForeignKey(User, max_length=30, blank=True, null=True)
    content = models.TextField(_(u'Content'), )
    content_highlighted = models.TextField(_(u'Highlighted Content'),
                                           blank=True)
    lexer = models.CharField(_(u'Lexer'),
                             max_length=30,
                             choices=LEXER_LIST,
                             default=LEXER_DEFAULT)
    published = models.DateTimeField(_(u'Published'), blank=True)
    expires = models.DateTimeField(_(u'Expires'), blank=True, help_text='asdf')
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children')
    num_views = models.IntegerField(default=0)

    class Meta:
        ordering = ('-published',)

    def get_linecount(self):
        return len(self.content.splitlines())

    def content_splitted(self):
        return self.content_highlighted.splitlines()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.published = datetime.datetime.now()
            self.secret_id = generate_secret_id()
        self.content_highlighted = pygmentize(self.content, self.lexer)
        super(Snippet, self).save(*args, **kwargs)

    def get_title(self):
        return self.title or _('Snippet #%d' % self.id)

    @permalink
    def get_absolute_url(self):
        return ('snippet_details', (self.secret_id,))

    def __unicode__(self):
        return '%s' % self.secret_id

mptt.register(Snippet, order_insertion_by=['content'])


class CodeLanguage(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return name
