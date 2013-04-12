from django.db import models
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition
from bcpp_subject.models import SubjectVisit
from packing_list import PackingList


class SubjectRequisition(BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    history = AuditTrail()

    def get_visit(self):
        return self.patient_visit

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
