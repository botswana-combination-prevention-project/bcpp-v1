from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model.fields import OtherCharField

from ..choices import WHERE_HIV_TEST_CHOICE, WHY_HIV_TEST_CHOICE

from .hiv_testing_supplemental import HivTestingSupplemental
from .crf_model_mixin import CrfModelMixin


class HivTested (HivTestingSupplemental):

    """CS002- for those who have tested for HIV. Its branch off from Q18 - HIV testing History"""

    num_hiv_tests = models.IntegerField(
        verbose_name="How many times before today have you had an HIV test?",
        null=True,
        help_text="",
    )

    where_hiv_test = models.CharField(
        verbose_name="Where were you tested for HIV, the last"
                     " [most recent] time you were tested?",
        max_length=85,
        choices=WHERE_HIV_TEST_CHOICE,
        help_text="",
    )
    where_hiv_test_other = OtherCharField()

    why_hiv_test = models.CharField(
        verbose_name="Not including today's HIV test, which of the following"
                     " statements best describes the reason you were tested the last"
                     " [most recent] time you were tested before today?",
        max_length=105,
        null=True,
        choices=WHY_HIV_TEST_CHOICE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Tested"
        verbose_name_plural = "HIV Tested"
