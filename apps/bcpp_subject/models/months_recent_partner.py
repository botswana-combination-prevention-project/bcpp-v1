from edc.audit.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner


class MonthsRecentPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"
