from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import WHERECIRC_CHOICE, WHYCIRC_CHOICE
#from base_scheduled_visit_model import BaseScheduledVisitModel
from base_circumcision import BaseCircumcision


class Circumcised (BaseCircumcision):
    
    """CS002"""
    
    whencirc = models.IntegerField(
        verbose_name = "74. At what age where you circumcised?",
        max_length = 2,
        null=True,
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond.",
        )

    wherecirc = models.CharField(
        verbose_name = "Supplemental MC10. Where were you circumcised?",
        max_length = 25,
        choices = WHERECIRC_CHOICE,
        help_text="",
        )

    whycirc = models.CharField(
        verbose_name = "Supplemental MC11. What was the main reason why were you circumcised?",
        max_length = 25,
        choices = WHYCIRC_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_circumcised_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
