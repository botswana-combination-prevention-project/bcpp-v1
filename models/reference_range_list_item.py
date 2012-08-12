from django.db import models

from audit_trail.audit import AuditTrail
from lab_reference.models import BaseReferenceListItem
from lab_reference.utils import get_lower_range_days, get_upper_range_days
from lab_clinic_api.models import TestCode
from reference_range_list import ReferenceRangeList


class ReferenceRangeListItem(BaseReferenceListItem):

    test_code = models.ForeignKey(TestCode)

    reference_range_list = models.ForeignKey(ReferenceRangeList)

    objects = models.Manager()

    history = AuditTrail()

    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    def __unicode__(self):
        return "{0}".format(self.test_code.code)

    class Meta:
        app_label = 'lab_clinic_reference'
        ordering = ['test_code', 'age_low', 'age_low_unit']
