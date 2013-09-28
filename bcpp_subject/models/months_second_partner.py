from edc_lib.audit_trail.audit import AuditTrail
from base_sexual_partner import BaseSexualPartner


class MonthsSecondPartner (BaseSexualPartner):

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Second Partner - 12 Months"
        verbose_name_plural = "Second Partner - 12 Months"
