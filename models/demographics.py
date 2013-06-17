from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp_list.models import LiveWith
from bcpp.choices import RELIGION_CHOICE, ETHNIC_CHOICE, MARITALSTATUS_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Demographics (BaseScheduledVisitModel):
    
    """CS002"""
    
    religion = models.CharField(
        verbose_name = "7. What is your religion affiliation?",
        max_length = 15,
        choices = RELIGION_CHOICE,
        help_text="",
        )

    ethnic = models.CharField(
        verbose_name = "8. What is your ethnic group?",
        max_length = 15,
        choices = ETHNIC_CHOICE,
        help_text="",
        )

    maritalstatus = models.CharField(
        verbose_name = "9. What is your current marital status?",
        max_length = 15,
        choices = MARITALSTATUS_CHOICE,
        help_text="",
        )

    numwives = models.IntegerField(
        verbose_name = ("10. How many wives do (you/your husband) have (including traditional marriage),"
                        " including yourself?"),
        max_length = 2,
        null=True, 
        blank=True,
        help_text="Note:leave blank if participant does not want to respond.",
        )

    livewith = models.ManyToManyField(LiveWith,
        verbose_name = "11. Who do you currently live with ?",
        null=True, 
        blank=True,
        help_text="[indicate all that apply]",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_demographics_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Demographics"
        verbose_name_plural = "Demographics"
