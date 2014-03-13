from edc.audit.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy


class RBDOffStudy(BaseOffStudy):

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_rbd"
        verbose_name = "RBD subject Off Study"
        verbose_name_plural = "RBD Subject Off Study"
