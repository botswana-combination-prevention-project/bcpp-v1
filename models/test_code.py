from django.db import models
from lab_test_code.models import TestCodeGroup
from base_test_code import BaseTestCode


class TestCode(BaseTestCode):

    test_code_group = models.ForeignKey(TestCodeGroup)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ['name']
        app_label = 'lab_test_code'
        db_table = 'bhp_lab_test_code_testcode'
