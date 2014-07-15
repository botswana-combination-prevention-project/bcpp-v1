from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future

from apps.bcpp.choices import ELISA_HIV_RESULT
from apps.bcpp_lab.models import SubjectRequisition

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .hic_enrollment import HicEnrollment


class ElisaHivResult (BaseScheduledVisitModel):

    hiv_result = models.CharField(
        verbose_name=_("HIV test result from the Elisa"),
        max_length=50,
        choices=ELISA_HIV_RESULT,
        )

    hiv_result_datetime = models.DateTimeField(
        verbose_name=_("HIV test result from the Elisa date and time"),
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
                raise exception_cls('Result cannot be changed. HIC Enrollment form exists for this subject. Got {0}'.format(self.hiv_result))

    def elisa_requisition_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
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
