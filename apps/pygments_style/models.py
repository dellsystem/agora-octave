from django.db import models


class PygmentsStyle(models.Model):
    """
    For allowing users to choose between syntax highlighting styles.

    Affects viewing snippets but not creating them. Users can set a
    default and can change the style when viewing specific snippets or
    files if necessary.
    """
    class_name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.class_name
