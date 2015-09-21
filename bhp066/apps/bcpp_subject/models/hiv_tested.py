from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import WHEREHIVTEST_CHOICE, WHYHIVTEST_CHOICE

from .hiv_testing_supplemental import HivTestingSupplemental
from .subject_consent import SubjectConsent


class HivTested (HivTestingSupplemental):

    """CS002- for those who have tested for HIV. Its branch off from Q18 - HIV testing History"""

    CONSENT_MODEL = SubjectConsent

    num_hiv_tests = models.IntegerField(
        verbose_name="How many times before today have you had an HIV test?",
        max_length=2,
        null=True,
        help_text="supplemental",
    )

    where_hiv_test = models.CharField(
        verbose_name="Where were you tested for HIV, the last"
                     " [most recent] time you were tested?",
        max_length=85,
        choices=WHEREHIVTEST_CHOICE,
        help_text="",
    )
    where_hiv_test_other = OtherCharField()

    why_hiv_test = models.CharField(
        verbose_name="Not including today's HIV test, which of the following"
                     " statements best describes the reason you were tested the last"
                     " [most recent] time you were tested before today?",
        max_length=105,
        null=True,
        choices=WHYHIVTEST_CHOICE,
        help_text="supplemental",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Tested"
        verbose_name_plural = "HIV Tested"
