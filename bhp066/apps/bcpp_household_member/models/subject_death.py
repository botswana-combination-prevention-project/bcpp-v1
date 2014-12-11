from edc.audit.audit_trail import AuditTrail

from .base_member_status_model import BaseMemberStatusModel


class SubjectDeath(BaseMemberStatusModel):

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.registered_subject)

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Subject Death"
        verbose_name_plural = "Subject Death"
