from django.db import models
from django.conf import settings
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition
from bcpp_subject.models import SubjectVisit
from packing_list import PackingList
from bcpp_inspector.models import SubjectRequisitionInspector


class SubjectRequisition(BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    history = AuditTrail()
    
    def save_to_inspector(self):
        SubjectRequisitionInspector.objects.create(
                subject_identifier = self.subject_identifier,
                requisition_datetime = self.requisition_datetime,
                requisition_identifier = self.requisition_identifier,
                specimen_identifier = self.specimen_identifier,
                device_id = settings.DEVICE_ID,
                app_name = 'bcpp_lab',
                model_name = 'SubjectRequisition'                
                )
    
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
