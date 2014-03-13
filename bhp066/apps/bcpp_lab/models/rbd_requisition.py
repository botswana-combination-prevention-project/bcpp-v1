from django.db import models

from edc.audit.audit_trail import AuditTrail
from apps.bcpp_rbd.models import RBDVisit

from ..models import BaseSubjectRequisition
from ..managers import RequisitionManager


class RBDRequisition(BaseSubjectRequisition):

    rbd_visit = models.ForeignKey(RBDVisit)

    entry_meta_data_manager = RequisitionManager(RBDVisit)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = self.rbd_visit.household_member.household_structure.household.plot.community
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(RBDRequisition, self).save(*args, **kwargs)

    def get_visit(self):
        return self.rbd_visit

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Blood Draw Only Requisition'
        unique_together = ('rbd_visit', 'panel', 'is_drawn')
