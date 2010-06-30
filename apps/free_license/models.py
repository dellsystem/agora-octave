from django.db import models

class FreeLicense(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    text = models.TextField()
    gpl_compatible = models.BooleanField()
    def __unicode__(self):
        return self.name
