from django.core.exceptions import ValidationError
from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future

from bhp066.apps.bcpp.choices import ELISA_HIV_RESULT

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .hic_enrollment import HicEnrollment


class ElisaHivResult (BaseScheduledVisitModel):

    hiv_result = models.CharField(
        verbose_name="HIV test result from the Elisa",
        max_length=50,
        choices=ELISA_HIV_RESULT,
    )

    hiv_result_datetime = models.DateTimeField(
        verbose_name="HIV test result from the Elisa date and time",
        null=True,
        blank=True,
        validators=[datetime_not_future],
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.hic_enrollment_checks()
        self.elisa_requisition_checks()
        super(ElisaHivResult, self).save(*args, **kwargs)

    def hic_enrollment_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit=self.subject_visit).exists():
            if self.hiv_result.lower() != 'neg':
                raise exception_cls('Result cannot be changed. HIC Enrollment form exists '
                                    'for this subject. Got {0}'.format(self.hiv_result))

    def elisa_requisition_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        SubjectRequisition = models.get_model('bcpp_lab', 'SubjectRequisition')
        if not SubjectRequisition.objects.filter(subject_visit=self.subject_visit, panel__name='ELISA').exists():
            raise exception_cls('ELISA Result cannot be saved before an ELISA Requisition is requested.')

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Elisa\'s HIV Result"
        verbose_name_plural = "Elisa\'s HIV Result"
