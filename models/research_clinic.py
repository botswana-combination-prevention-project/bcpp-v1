from django.db import models
from bhp_research_protocol.models import Site, Protocol

class ResearchClinic(models.Model):

    site = models.ForeignKey(Site)

    protocol = models.OneToOneField(Protocol)

    clinic_name = models.CharField(
        max_length=35,
        unique=True,
        )

    def __unicode__(self):
        return '%s %s' % (self.site.site_identifier, self.clinic_name)
        
    class Meta:
        ordering = ['research_name']
        app_label = 'bhp_research_protocol'        
