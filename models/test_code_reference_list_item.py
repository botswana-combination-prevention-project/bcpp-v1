from django.db import models
from bhp_lab_reference.models import BaseReferenceListItem
from bhp_lab_reference.utils import get_lower_range_days, get_upper_range_days
from bhp_lab_test_code.models import TestCodeReferenceList
from audit_trail import audit

class TestCodeReferenceListItem(BaseReferenceListItem):

    test_code_reference_list = models.ForeignKey(TestCodeReferenceList)
    
    history = audit.AuditTrail()
    
    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    def __unicode__(self):
        return "%s" % (self.test_code)
    
    class Meta:
        app_label = 'bhp_lab_test_code'  
        ordering = ['test_code', 'age_low', 'age_low_unit']   
