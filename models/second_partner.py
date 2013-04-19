from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from detailed_sexual_history import DetailedSexualHistory


class SecondPartner (DetailedSexualHistory):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_secondpartner_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Second Partner"
        verbose_name_plural = "CS003: Second Partner"
