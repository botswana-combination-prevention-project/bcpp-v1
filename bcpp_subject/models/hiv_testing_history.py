from django.db import models
from django.utils.translation import ugettext as _
from edc_lib.audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO, YES_NO_DONT_ANSWER, WHENHIVTEST_CHOICE, VERBALHIVRESULT_CHOICE
from bcpp_subject.choices import YES_NO_RECORD_REFUSAL
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingHistory (BaseScheduledVisitModel):

    has_tested = models.CharField(
        verbose_name=_("Have you ever been tested for HIV before?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    when_hiv_test = models.CharField(
        verbose_name=_("When was the last [most recent]"
                        " time you were tested for HIV?"),
        max_length=25,
        null=True,
        blank=True,
        choices=WHENHIVTEST_CHOICE,
        help_text="(verbal response)",
        )

    has_record = models.CharField(
        verbose_name=_("Is a record of last HIV test [OPD card, Tebelopele,"
                      " other] available to review?"),
        max_length=45,
        null=True,
        blank=True,
        choices=YES_NO_RECORD_REFUSAL,
        help_text="if no card available for viewing, proceed to next question",
        )

    verbal_hiv_result = models.CharField(
        verbose_name=_("Please tell me the results of your last [most recent] HIV test?"),
        max_length=30,
        null=True,
        blank=True,
        choices=VERBALHIVRESULT_CHOICE,
        help_text="(verbal response)",
        )

    other_record = models.CharField(
        verbose_name=_("Do you have any other available documentation of an HIV result?"),
        max_length=3,
        null=True,
        blank=True,
        choices=YES_NO,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Testing History"
        verbose_name_plural = "HIV Testing History"
