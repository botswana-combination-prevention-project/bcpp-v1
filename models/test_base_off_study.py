from audit_trail.audit import AuditTrail
from bhp_off_study.models import BaseOffStudy


class TestBaseOffStudy(BaseOffStudy):
    """ Test Off-Study."""

    history = AuditTrail()

    def __unicode__(self):
        return '{0} '.format(self.registered_subject)

    class Meta:
        app_label = "bhp_base_test"
