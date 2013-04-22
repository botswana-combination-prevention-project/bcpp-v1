from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import ALCOHOL_CHOICE, YES_NO_DONT_ANSWER
from base_scheduled_visit_model import BaseScheduledVisitModel


class SubstanceUse (BaseScheduledVisitModel):
    
    """CS002"""
    
    alcohol = models.CharField(
        verbose_name=("99. In the past month, how often did you consume alcohol?"
                      "  [If you don't know exactly, give your best guess.]"),
        max_length = 15,
        choices = ALCOHOL_CHOICE,
        help_text="",
        )

    smoke = models.CharField(
        verbose_name = "100. Do you currently smoke any tobacco products, such as cigarettes, cigars, or pipes?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_substanceuse_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Substance Use"
        verbose_name_plural = "Substance Use"
