from django.db import models
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition
from bhp_base_test.models import TestVisit


class TestRequisition(BaseRequisition):

    test_visit = models.ForeignKey(TestVisit)

    history = AuditTrail()

    class Meta:
        app_label = 'bhp_base_test'
