from django.db import models

from simple_history.models import HistoricalRecords

from ..choices import WHY_NO_HIV_TESTING_CHOICE

from .hiv_testing_supplemental import HivTestingSupplemental
from .crf_model_mixin import CrfModelMixin


class HivUntested (HivTestingSupplemental):

    """CS002- for those who have NOT tested for HIV. Its
    branch off from Q18 - HIV testing History"""

    why_no_hiv_test = models.CharField(
        verbose_name="If you were not tested for HIV in the 12 months prior"
                     " to today, what is the main reason why not?",
        max_length=55,
        null=True,
        choices=WHY_NO_HIV_TESTING_CHOICE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Untested"
        verbose_name_plural = "HIV Untested"
