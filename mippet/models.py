from django.db import models

# Create your models here.

class free_license(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    text = models.TextField()
    gpl_compatible = models.BooleanField()
    def __unicode__(self):
        return self.name
    

class mscript(models.Model):
    name = models.CharField(max_length=512)
    code = models.TextField()
    free_license = models.ForeignKey(free_license)
    underlying_file = models.FileField(upload_to="var/")
    is_standalone = models.BooleanField()
    def __unicode__(self):
        return self(name)

class bundle(models.Model):
    name = models.CharField(max_length=512)
    script = mscript()
    def __unicode__(self):
        return self(name)
