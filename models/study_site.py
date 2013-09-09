from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_variables.managers import StudySiteManager


class StudySite(BaseUuidModel):

    site_code = models.CharField(max_length=4, unique=True)

    site_name = models.CharField(max_length=35, unique=True)

    objects = StudySiteManager()

    def natural_key(self):
        return (self.site_code, )

    def __unicode__(self):
        return "%s %s" % (self.site_code, self.site_name)

    class Meta:
        unique_together = [('site_code', 'site_name')]
        ordering = ['site_code', ]
        app_label = 'bhp_variables'
