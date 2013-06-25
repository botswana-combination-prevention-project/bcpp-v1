from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import WHYNOHIVTESTING_CHOICE
# from base_scheduled_visit_model import BaseScheduledVisitModel
from hiv_testing_supplemental import HivTestingSupplemental


class HivUntested (HivTestingSupplemental):
    
    """CS002- for those who have NOT tested for HIV. Its branch off from Q18 - HIV testing History"""
    
    whynohivtest = models.CharField(
        verbose_name=("Supplemental HT4. If you were not tested for HIV in the 12 months prior"
                      " to today, what is the main reason why not?"),
        max_length=55,
        null=True, 
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivuntested_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Untested"
        verbose_name_plural = "HIV Untested"
