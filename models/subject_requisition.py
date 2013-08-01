from django.db import models
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition
from bcpp_subject.models import SubjectVisit
from packing_list import PackingList


class SubjectRequisition(BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(SubjectRequisition, self).save(*args, **kwargs)

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
