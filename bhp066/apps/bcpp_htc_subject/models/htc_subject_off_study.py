from django.db.models import get_model
from edc_base.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy


class HtcSubjectOffStudy(BaseOffStudy):

    history = AuditTrail()

    def dispatch_container_lookup(self, using=None):
        HtcRegistration = get_model('bcpp_htc_subject', 'HtcRegistration')
        return (HtcRegistration, 'registered_subject__subject_identifier')

    class Meta:
        app_label = "bcpp_htc_subject"
        verbose_name = "HTC Subject Off-Study"
        verbose_name_plural = "HTC Subject Off-Study"
