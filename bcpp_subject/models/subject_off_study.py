from audit_trail.audit import AuditTrail
from bhp_off_study.models import BaseOffStudy


class SubjectOffStudy(BaseOffStudy):

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Off Study"
        verbose_name_plural = "Subject Off Study"
