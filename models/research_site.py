from django.db import models

class ResearchSite(models.Model):

    site = models.ForeignKey(Site)

    protocol = models.OneToOneField(Protocol)

    research_name = models.CharField(
        max_length=35,
        unique=True,
        )

    def __unicode__(self):
        return '%s %s' % (self.site.code, self.research_name)
        
    class Meta:
        ordering = ['research_name']
        app_label = 'bhp_research_protocol'        
