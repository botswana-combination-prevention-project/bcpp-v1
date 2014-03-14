from edc.audit.audit_trail import AuditTrail
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from edc.subject.consent.mixins.bw import IdentityFieldsMixin

from apps.bcpp_subject.models import BaseSubjectConsent


class RBDConsent(BaseSubjectConsent):

    history = AuditTrail()

    def bypass_for_edit_dispatched_as_item(self):
        return True

    class Meta:
        app_label = 'bcpp_rbd'
        verbose_name = 'RBD Consent'
        unique_together = ('subject_identifier', 'survey')

# add Mixin fields to abstract class
for field in IdentityFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)

for field in ReviewAndUnderstandingFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)