from edc_base.audit_trail import AuditTrail

from .detailed_sexual_history import DetailedSexualHistory


class ThirdPartner (DetailedSexualHistory):

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Third Partner"
        verbose_name_plural = "CS003: Third Partner"
