from edc.audit.audit_trail import AuditTrail
from edc.subject.lab_tracker.classes import site_lab_tracker

from ..models import BaseHouseholdMemberConsent

from .subject_consent_history import SubjectConsentHistory
from .subject_off_study_mixin import SubjectOffStudyMixin


class SubjectConsentRbd(SubjectOffStudyMixin, BaseHouseholdMemberConsent):

    history = AuditTrail()

    def get_subject_type(self):
        return 'subject'

    def get_consent_history_model(self):
        return SubjectConsentHistory

    def get_registered_subject(self):
        return self.registered_subject

    def get_hiv_status(self):
        """Returns the hiv testing history as a string.

        .. note:: more than one table is tracked so the history includes HIV results not performed by our team
                  as well as the results of tests we perform."""
        return site_lab_tracker.get_history_as_string('HIV', self.subject_identifier, 'subject')

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ('subject_identifier', 'survey')
