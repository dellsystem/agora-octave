from django.db import models

class Free_license(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    text = models.TextField()
    gpl_compatible = models.BooleanField()
    def __unicode__(self):
        return self.name
