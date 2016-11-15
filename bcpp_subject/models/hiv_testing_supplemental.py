from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_UNSURE

from .crf_model_mixin import CrfModelMixin


class HivTestingSupplemental (CrfModelMixin):

    hiv_pills = models.CharField(
        verbose_name="Have you ever heard about treatment for"
                     " HIV with pills called antiretroviral therapy or ARVs [or HAART]?",
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="",
    )

    arvs_hiv_test = models.CharField(
        verbose_name="Do you believe that treatment for HIV with "
                     "antiretroviral therapy (or ARVs) can help HIV-positive people"
                     " to live longer?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_UNSURE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        abstract = True
