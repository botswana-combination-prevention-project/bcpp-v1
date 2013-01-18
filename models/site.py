from django.db import models
from bhp_research_protocol.models import Location


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
        return '%s' % (self.site_identifier)

    class Meta:
        ordering = ['site_identifier']
        app_label = 'bhp_research_protocol'
