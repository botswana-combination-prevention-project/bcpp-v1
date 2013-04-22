from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Circumcision (BaseScheduledVisitModel):
    
    """CS002"""
    
    circumcised = models.CharField(
        verbose_name = "72. Are you circumcised?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_circumcision_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcision"
        verbose_name_plural = "Circumcision"
