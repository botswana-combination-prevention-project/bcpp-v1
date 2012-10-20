from django.db import models
from lab_panel.models import BasePanel
from test_code import TestCode
from lab_clinic_api.choices import PANEL_TYPE


class Panel(BasePanel):

    edc_name = models.CharField(max_length=50, null=True)

    test_code = models.ManyToManyField(TestCode, null=True, blank=True)

    panel_type = models.CharField(max_length=15, choices=PANEL_TYPE, default='TEST')

    objects = models.Manager()

    def __unicode__(self):
        return self.edc_name

    def save(self, *args, **kwargs):
        if not self.edc_name:
            self.edc_name = self.name
        super(Panel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lab_clinic_api'
