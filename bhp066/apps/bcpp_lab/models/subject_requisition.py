from django.db import models

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_subject.models import SubjectVisit

from ..models import BaseBcppRequisition
from ..managers import RequisitionManager


class SubjectRequisition(BaseBcppRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    entry_meta_data_manager = RequisitionManager(SubjectVisit)

    history = AuditTrail()

    def get_visit(self):
        return self.subject_visit

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
        unique_together = ('subject_visit', 'panel', 'is_drawn')
