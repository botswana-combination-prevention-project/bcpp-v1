from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.choices import YES_NO_NA

from bhp066.apps.bcpp.choices import YES_NO_DWTA, WHENHIVTEST_CHOICE, VERBALHIVRESULT_CHOICE

from ..choices import YES_NO_RECORD_REFUSAL

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class HivTestingHistory (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    has_tested = models.CharField(
        verbose_name="Have you ever been tested for HIV before?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
    )

    when_hiv_test = models.CharField(
        verbose_name="When was the last [most recent]"
                     " time you were tested for HIV?",
        max_length=25,
        null=True,
        blank=True,
        choices=WHENHIVTEST_CHOICE,
        help_text="(verbal response)",
    )

    # this field triggers HivTestReview
    has_record = models.CharField(
        verbose_name="Is a record of last [most recent] HIV test [OPD card, Tebelopele,"
                     " other] available to review?",
        max_length=45,
        null=True,
        blank=True,
        choices=YES_NO_RECORD_REFUSAL,
        help_text="if no card available for viewing, proceed to next question",
    )

    # used by admin_supplemental fields for HIV status condition??
    verbal_hiv_result = models.CharField(
        verbose_name="Please tell me the results of your last [most recent] HIV test?",
        max_length=30,
        null=True,
        blank=True,
        choices=VERBALHIVRESULT_CHOICE,
        help_text="(verbal response)",
    )

    # this field triggers HivResultDocumentation
    other_record = models.CharField(
        verbose_name="Do you have any other available documentation of positive HIV status?",
        max_length=3,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        default=YES_NO_NA[2][0],
        help_text="This documentation refers to: PMTCT prescription, ART, CD4 count record, lab result for.. etc",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Testing History"
        verbose_name_plural = "HIV Testing History"
