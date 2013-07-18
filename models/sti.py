from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp_subject.choices import STI_DX  
from base_scheduled_visit_model import BaseScheduledVisitModel


class Sti (BaseScheduledVisitModel):
    
    """CS002 - Medical Diagnoses - Sti"""

    sti_date = models.DateField(
        verbose_name="Date of the diagnosis of the STI (Sexually transmitted infection):",
        help_text="",
        )

    sti_dx = models.CharField(
        verbose_name="[Interviewer:] What is the STI diagnosed as recorded?",
        max_length=65,
        choices=STI_DX,
        help_text="",
        )
    
    comments = models.CharField(
        verbose_name="Comments",
        max_length=250,
        null=True,
        blank=True,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_sti_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "STI\'s"
        verbose_name_plural = "STI\'s"
