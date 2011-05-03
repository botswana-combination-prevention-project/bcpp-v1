from django.db import models


class Site(models.Model):

    site_identifier = models.CharField(
        max_length=25,
        unique=True,
        )

    name = models.CharField(
        max_length=25,
        unique=True,
        )

    location = models.ForeignKey(Location)

    def __unicode__(self):
        return '%s %s' % (self.code, self.name)
        
    class Meta:
        ordering = ['name']
        app_label = 'bhp_research_protocol'
        

