from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future
from edc.choices import YES_NO_NA
from apps.bcpp.choices import HIV_RESULT, WHYNOHIVTESTING_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .hic_enrollment import HicEnrollment


class HivResult (BaseScheduledVisitModel):

    hiv_result = models.CharField(
        verbose_name=("Today\'s HIV test result"),
        max_length=50,
        choices=HIV_RESULT,
        help_text="If participant declined HIV testing, please select a reason below.",
        )

    hiv_result_datetime = models.DateTimeField(
        verbose_name=("Today\'s HIV test result date and time"),
        null=True,
        blank=True,
        validators=[datetime_not_future],
        )

    blood_draw_type = models.CharField(
        verbose_name=("What type of blood was used for the test"),
        max_length=15,
        choices=(('capillary', 'Capillary'), ('venous', 'Venous'), ('N/A', 'Not applicable')),
        default='N/A',
        help_text="",
        )

    insufficient_vol = models.CharField(
        verbose_name='If capillary, is the volume less than 350uL?',
        max_length=15,
        choices=YES_NO_NA,
        default='N/A',
        help_text='Note: if capillary blood and less than 350uL, an additional venous blood draw is required'
        )

    why_not_tested = models.CharField(
        verbose_name=_("What was the main reason why you did not want HIV testing"
                       " as part of today's visit?"),
        max_length=65,
        null=True,
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.hic_enrollment_checks(self, self.subject_visit)
        super(HivResult, self).save(*args, **kwargs)

    def hic_enrollment_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit=self.subject_visit).exists():
            if self.hiv_result.lower() != 'neg':
                raise exception_cls('Result cannot be changed. HIC Enrollment form exists for this subject. Got {0}'.format(self.hiv_result))

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Today\'s HIV Result"
        verbose_name_plural = "Today\'s HIV Result"
