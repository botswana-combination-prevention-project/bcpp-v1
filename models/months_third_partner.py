from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from base_sexual_partner import BaseSexualPartner


class MonthsThirdPartner (BaseSexualPartner):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_monthsthirdpartner_change', args=(self.id,))
    
    
    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Third Partner - 12 Months"
        verbose_name_plural = "Third Partner - 12 Months"
