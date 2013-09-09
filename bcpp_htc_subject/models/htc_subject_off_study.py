from django.db.models import get_model
from audit_trail.audit import AuditTrail
from bhp_off_study.models import BaseOffStudy


class HtcSubjectOffStudy(BaseOffStudy):

    history = AuditTrail()

    def dispatch_container_lookup(self, using=None):
        HtcRegistration = get_model('bcpp_htc', 'HtcRegistration')
        return (HtcRegistration, 'registered_subject__subject_identifier')

    class Meta:
        app_label = "bcpp_htc_subject"
        verbose_name = "HTC Subject Off-Study"
        verbose_name_plural = "HTC Subject Off-Study"
