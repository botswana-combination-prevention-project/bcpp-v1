from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import LOWESTCD4_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivMedicalCare (BaseScheduledVisitModel):
    
    """CS002"""
    
    firsthivcarepositive = models.DateField(
        verbose_name="60. When did you first receive HIV-related medical care?",
        max_length=25,
        help_text=("Note: If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, leave blank."),
        )

    lasthivcarepositive = models.DateField(
        verbose_name="61. When did you last (most recently) receive HIV-related medical care?",
        max_length=25,
        help_text=("Note: If participant does not want to answer,leave blank. "
                   "If participant is unable to estimate date, leave blank."),
        )

    lowestCD4 = models.CharField(
        verbose_name="62. What was your lowest CD4 (masole) count that was ever measured?",
        max_length=25,
        choices=LOWESTCD4_CHOICE,
        help_text=("Note:Assist the participant by helping review their outpatient cards if "
                   "they are available."),
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivmedicalcare_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Medical care"
        verbose_name_plural = "HIV Medical care"
