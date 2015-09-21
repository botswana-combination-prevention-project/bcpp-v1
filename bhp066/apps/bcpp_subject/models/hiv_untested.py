from django.db import models

from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp.choices import WHYNOHIVTESTING_CHOICE

from .hiv_testing_supplemental import HivTestingSupplemental
from .subject_consent import SubjectConsent

class HivUntested (HivTestingSupplemental):

    """CS002- for those who have NOT tested for HIV. Its
    branch off from Q18 - HIV testing History"""

    CONSENT_MODEL = SubjectConsent

    why_no_hiv_test = models.CharField(
        verbose_name="If you were not tested for HIV in the 12 months prior"
                     " to today, what is the main reason why not?",
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
