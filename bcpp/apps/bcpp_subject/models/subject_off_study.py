from edc_base.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy
from edc.device.dispatch.models import BaseDispatchSyncUuidModel


class SubjectOffStudy(BaseOffStudy, BaseDispatchSyncUuidModel):

    """A model completed by the user that completed when the subject is taken off-study."""

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Off Study"
        verbose_name_plural = "Subject Off Study"
