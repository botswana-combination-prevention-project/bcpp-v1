from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import WHEREHIVTEST_CHOICE, WHYHIVTEST_CHOICE
# from base_scheduled_visit_model import BaseScheduledVisitModel
from hiv_testing_supplemental import HivTestingSupplemental


class HivTested (HivTestingSupplemental):

    """CS002- for those who have tested for HIV. Its branch off from Q18 - HIV testing History"""

    num_hiv_tests = models.IntegerField(
        verbose_name="Supplemental HT1. How many times before today have you had an HIV test?",
        max_length=2,
        null=True,
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond.",
        )

    where_hiv_test = models.CharField(
        verbose_name=("Supplemental HT2. Where were you tested for HIV, the last"
                      " [most recent] time you were tested?"),
        max_length=85,
        null=True,
        blank=True,
        choices=WHEREHIVTEST_CHOICE,
        help_text="",
        )

    why_hiv_test = models.CharField(
        verbose_name=("Supplemental HT3. Not including today's HIV test, which of the following"
                      " statements best describes the reason you were tested the last"
                      " [most recent] time you were tested before today?"),
        max_length=105,
        null=True,
        blank=True,
        choices=WHYHIVTEST_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtested_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Tested"
        verbose_name_plural = "HIV Tested"
