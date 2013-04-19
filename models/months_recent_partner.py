from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from base_sexual_partner import BaseSexualPartner


class MonthsRecentPartner (BaseSexualPartner):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_monthsrecentpartner_change', args=(self.id,))
    
    
    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"
