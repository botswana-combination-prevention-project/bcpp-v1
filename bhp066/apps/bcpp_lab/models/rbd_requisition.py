from django.db import models

from edc.audit.audit_trail import AuditTrail
from apps.bcpp_rbd.models import RBDVisit

from ..models import BaseBcppRequisition
from ..managers import RequisitionManager


class RBDRequisition(BaseBcppRequisition):

    rbd_visit = models.ForeignKey(RBDVisit)

    entry_meta_data_manager = RequisitionManager(RBDVisit)

    history = AuditTrail()

    def get_visit(self):
        return self.rbd_visit

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Blood Draw Only Requisition'
        unique_together = ('rbd_visit', 'panel', 'is_drawn')
