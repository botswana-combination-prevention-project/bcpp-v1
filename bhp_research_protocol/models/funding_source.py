from django.db import models


class FundingSource(models.Model):

    name = models.CharField(max_length=25)

    reference = models.CharField(max_length=25, blank=True)

    description = models.TextField(
        max_length=500,
        )    

    def __unicode__(self):
        return '%s %s' % (self.name, self.reference)
        
    class Meta:
        ordering = ['name']
        app_label = 'bhp_research_protocol'

