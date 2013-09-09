from django.db import models


class Sponsor(models.Model):

    name = models.CharField(max_length=50)

    description = models.CharField(
        max_length=250,
        )

    contact_name = models.EmailField(
        blank=True,
        )

    contact_tel = models.CharField(
        max_length=50,
        blank=True,
        )

    contact_email = models.EmailField(
        blank=True,
        )

    def __unicode__(self):
        return '%s %s' % (self.name, self.reference)

    class Meta:
        ordering = ['name']
        app_label = 'bhp_research_protocol'
