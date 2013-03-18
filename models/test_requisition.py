from django.db import models
from audit_trail.audit import AuditTrail
from lab_requisition.models import BaseRequisition
from bhp_visit_tracking.models import TestSubjectVisit


class TestRequisition(BaseRequisition):

    test_subject_visit = models.ForeignKey(TestSubjectVisit)

    history = AuditTrail()

    class Meta:
        app_label = 'lab_requisition'
