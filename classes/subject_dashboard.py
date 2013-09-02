from base_subject_dashboard import BaseSubjectDashboard
from bcpp_subject.models import SubjectConsent, SubjectVisit, SubjectLocator
from bcpp_lab.models import SubjectRequisition, PackingList


class SubjectDashboard(BaseSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_name = 'Subject Dashboard'

    def __init__(self, **kwargs):
        self._delivery_datetime = None
        self.dashboard_type = 'subject'
        self.exclude_others_if_keyed_model_name = 'subjectconsent'  # TODO: is this needed??
        kwargs.update({'dashboard_models': {'subject_consent': SubjectConsent}})
        super(SubjectDashboard, self).__init__(**kwargs)

#     def set_membership_form_category(self):
#         self._membership_form_category = 'subject'

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['subject']

    def set_consent(self):
        self._consent = SubjectConsent.objects.get(subject_identifier=self.get_subject_identifier())

    def get_visit_model(self):
        return SubjectVisit

    def get_requisition_model(self):
        return SubjectRequisition

    def get_locator_model(self):
        return SubjectLocator

    def get_locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000'

    def get_packing_list_model(self):
        return PackingList
