from django.db import models
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition


class TestRequisition(BaseRequisition):

    history = AuditTrail()

    class Meta:
        app_label = 'lab_requisition'
