from django.db import models
from django.utils.translation import ugettext as _
from bcpp.choices import YES_NO_DONT_ANSWER, PREGARV_CHOICE, YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class BasePregnancy (BaseScheduledVisitModel):

    """CS002"""

    last_birth = models.DateField(
        verbose_name=_("When did you last (most recently) give birth?"),
        null=True, 
        blank=True,
        help_text="",
        )

    anc_last_pregnancy = models.CharField(
        verbose_name=_("During your last pregnancy (not current pregnancy) did you go for antenatal care?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        null=True, 
        blank=True,
        help_text="",
        )

    hiv_last_pregnancy = models.CharField(
        verbose_name=_("During your last pregnancy (not current pregnancy) were you tested for HIV?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        blank=True,
        help_text="If respondent was aware that she was HIV-positive prior to last pregnancy",
        )

    preg_arv = models.CharField(
        verbose_name=_("Were you given antiretroviral medications to protect the baby?"),
        max_length=95,
        choices=PREGARV_CHOICE,
        null=True,
        blank=True,
        help_text="",
        )

    class Meta:
        abstract = True
