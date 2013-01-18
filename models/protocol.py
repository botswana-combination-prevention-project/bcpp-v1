from django.db import models
from bhp_research_protocol.models import FundingSource


class Protocol(models.Model):

    protocol_identifier = models.CharField(
        max_length=25,
        null=True,
        )

    research_title = models.TextField(max_length=250)

    short_title = models.CharField(max_length=25)

    site_name_fragment = models.CharField(max_length=25,
        help_text='Fragment of proper site name not including BHP protocol number or location'
        )

    # site = models.ManyToManyField(Site)

    local_title = models.CharField(max_length=25, blank=True)

    # prinicipal_investigator = models.ManyToManyField(PrincipalInvestigator)

    # site_leader = models.ManyToManyField(SiteLeader)

    funding_source = models.ManyToManyField(FundingSource)

    date_registered = models.DateField(
        verbose_name="Date registered with BHP",
        )

    date_opened = models.DateField(
        verbose_name="Date opened",
        )

    description = models.TextField(
        max_length=500,
        )

    def get_absolute_url(self):
        return "/bhp_research_protocol/protocol/%s/" % self.id

    def __unicode__(self):
        return self.protocol_identifier

    class Meta:
        ordering = ['protocol_identifier']
        app_label = 'bhp_research_protocol'
