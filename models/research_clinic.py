from django.db import models
from bhp_research_protocol.models import Site, Protocol


class ResearchClinic(models.Model):

    site = models.ForeignKey(Site)

    protocol = models.OneToOneField(Protocol)

    name = models.CharField(
        max_length=35,
        unique=True,
        )

    def __unicode__(self):
        return '%s %s %s' % (self.site.site_identifier, self.name, self.site.location)

    class Meta:
        ordering = ['name']
        app_label = 'bhp_research_protocol'
