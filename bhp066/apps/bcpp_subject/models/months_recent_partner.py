from edc.audit.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner


class MonthsRecentPartner (BaseSexualPartner):

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"
