from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail

from apps.bcpp.choices import WHYNOHIVTESTING_CHOICE

from .hiv_testing_supplemental import HivTestingSupplemental


class HivUntested (HivTestingSupplemental):

    """CS002- for those who have NOT tested for HIV. Its
    branch off from Q18 - HIV testing History"""

    why_no_hiv_test = models.CharField(
        verbose_name=_("If you were not tested for HIV in the 12 months prior"
                       " to today, what is the main reason why not?"),
        max_length=55,
        null=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="supplemental",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Untested"
        verbose_name_plural = "HIV Untested"
