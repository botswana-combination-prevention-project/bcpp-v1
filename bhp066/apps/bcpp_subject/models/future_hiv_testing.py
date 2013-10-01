# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from apps.bcpp.choices import HIVTEST_PREFEREDWEEK, HIVTEST_PREFEREDYEAR, HIVTEST_PREFEREDTIME, HIVTESTPREFERENCE_CHOICE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class FutureHivTesting (BaseScheduledVisitModel):

    """CS002.

    Note to Interviewer: If participant is known to be HIV-infected"
    " (tested positive today or previously), skip to the next section. "
    "Read to Participant: The following questions are about how you would like"
    " to have HIV testing in the future. """

    prefer_hivtest = models.CharField(
        verbose_name=_("In the future, where would you prefer to get tested for HIV?"),
        max_length=70,
        null=True,
        choices=HIVTESTPREFERENCE_CHOICE,
        help_text="supplemental",
        )

    hiv_test_time = models.CharField(
        verbose_name=_("In the future, is there a particular time of day that"
                      " you would prefer to receive your next HIV test?"),
        max_length=35,
        choices=HIVTEST_PREFEREDTIME,
        null=True,
        help_text="supplemental",
        )
    hiv_test_time_other = OtherCharField(
        verbose_name=_("If yes, specify:"),
        null=True,
        )

    hiv_test_week = models.CharField(
        verbose_name=_("In the future, is there a particular day of the week"
                      " that you would prefer to receive your next HIV test?"),
        max_length=35,
        choices=HIVTEST_PREFEREDWEEK,
        null=True,
        help_text="supplemental",
        )
    hiv_test_week_other = OtherCharField(
        verbose_name=_("If yes, specify:"),
        null=True,
        )

    hiv_test_year = models.CharField(
        verbose_name=_("In the future, is there a particular time of year that"
                      " you would prefer to receive your next HIV test?"),
        max_length=25,
        choices=HIVTEST_PREFEREDYEAR,
        null=True,
        help_text="supplemental",
        )
    hiv_test_year_other = OtherCharField(
        verbose_name=_("If yes, specify:"),
        null=True,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Supp- Future HIV testing"
        verbose_name_plural = "Supp- Future HIV testing"
