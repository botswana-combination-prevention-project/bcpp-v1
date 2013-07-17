from django.db import models
from bcpp.choices import YES_NO_DONT_ANSWER, PREGARV_CHOICE, YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class BasePregnancy (BaseScheduledVisitModel):

    """CS002"""

    last_birth = models.DateField(
        verbose_name="When did you last (most recently) give birth?",
        help_text="",
        )

    anc_last_pregnancy = models.CharField(
        verbose_name="During your last pregnancy (not current pregnancy) did you go for antenatal care?",
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    hiv_last_pregnancy = models.CharField(
        verbose_name="During your last pregnancy (not current pregnancy) were you tested for HIV?",
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="If respondent was aware that she was HIV-positive prior to last pregnancy",
        )

    preg_arv = models.CharField(
        verbose_name="Were you given antiretroviral medications to protect the baby?",
        max_length=95,
        choices=PREGARV_CHOICE,
        null=True,
        help_text="",
        )
    
    class Meta:
        abstract = True
