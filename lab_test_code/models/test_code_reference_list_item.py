from django.db import models
from audit_trail.audit import AuditTrail
from lab_reference.models import BaseReferenceListItem
from lab_reference.utils import get_lower_range_days, get_upper_range_days
from test_code_reference_list import TestCodeReferenceList
from test_code import TestCode


class TestCodeReferenceListItem(BaseReferenceListItem):

    test_code = models.ForeignKey(TestCode)

    test_code_reference_list = models.ForeignKey(TestCodeReferenceList)

    objects = models.Manager()

    history = AuditTrail()

    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    def __unicode__(self):
        return "%s" % (self.test_code)

    class Meta:
        app_label = 'lab_test_code'
        db_table = 'bhp_lab_test_code_testcodereferencelistitem'
        ordering = ['test_code', 'age_low', 'age_low_unit']
