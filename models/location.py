from django.db import models

class Location(models.Model):

    name = models.CharField(
        max_length=25,
        unique=True,
        )

    def __unicode__(self):
        return '%s' % (self.name)
        
    class Meta:
        ordering = ['name']
        app_label = 'bhp_research_protocol'
        

