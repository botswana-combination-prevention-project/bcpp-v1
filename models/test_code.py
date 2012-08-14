from django.db import models
from lab_test_code.models import BaseTestCode
from test_code_group import TestCodeGroup


class TestCode(BaseTestCode):

    edc_code = models.CharField(max_length=25, null=True)

    edc_name = models.CharField(max_length=50, null=True)

    test_code_group = models.ForeignKey(TestCodeGroup, null=True)

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):

        if not self.edc_code:
            self.edc_code = self.code
        if not self.edc_name:
            self.edc_name = self.name
        super(TestCode, self).save(*args, **kwargs)

    class Meta:
        ordering = ["edc_code"]
        app_label = 'lab_clinic_api'
