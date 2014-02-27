from edc.audit.audit_trail import AuditTrail
from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from apps.bcpp_subject.models import BaseSubjectConsent


class SubjectConsentRBDonly(BaseSubjectConsent):

    history = AuditTrail()

    def bypass_for_edit_dispatched_as_item(self):
        return True

    class Meta:
        app_label = 'bcpp_rbd_subject'
<<<<<<< HEAD
        verbose_name = 'Subject Consent RBD only'
        verbose_name_plural = 'Subject Consent RBD only'
=======
        verbose_name = 'Blood Draw Consent RBD Only'
        verbose_name_plural = 'Blood Draw Consent RBD Only'
>>>>>>> 2692f8915f0746ef0cbe241092790d2c7c159195
        unique_together = ('subject_identifier', 'survey')

# add Mixin fields to abstract class
for field in IdentityFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)

for field in ReviewAndUnderstandingFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)