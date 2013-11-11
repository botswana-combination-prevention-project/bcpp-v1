from django.template.loader import render_to_string

from apps.bcpp_subject.models import SubjectConsent, SubjectVisit, SubjectLocator, SubjectReferral
from apps.bcpp_lab.models import SubjectRequisition, PackingList


from .base_subject_dashboard import BaseSubjectDashboard


class SubjectDashboard(BaseSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_name = 'Participant Dashboard'

    def __init__(self, *args, **kwargs):
        kwargs.update({'dashboard_models': {'subject_consent': SubjectConsent}})
        super(SubjectDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(SubjectDashboard, self).add_to_context()
        self.context.add(
            home='bcpp',
            search_name='subject',
            household_dashboard_url=self.get_household_dashboard_url(),
            title='Research Subject Dashboard',
            subject_consent=self.get_consent(),
            subject_referral=self.get_subject_referral(),
            rendered_household_members_sidebar=self.render_household_members_sidebar(),
            )

    def get_household_dashboard_url(self):
        return 'household_dashboard_url'

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['subject']

    def set_consent(self, subject_identifier):
        """Sets to the subject consent, if it has been completed."""
        self._consent = None
        if SubjectConsent.objects.filter(subject_identifier=subject_identifier):
            self._consent = SubjectConsent.objects.get(subject_identifier=subject_identifier)

    def get_subject_referral(self):
        if SubjectReferral.objects.filter(subject_visit=self.get_visit_model_instance()):
            return SubjectReferral.objects.get(subject_visit=self.get_visit_model_instance())
        return 'unknown referral'

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

    def render_labs(self, update=False):
        return ''

    def render_household_members_sidebar(self):
        """Renders to string the household members sidebar."""
        return render_to_string('household_members_sidebar.html',
            {'household_members': self.get_household_members(),
             'household_dashboard_url': self.get_household_dashboard_url(),
             'household_structure': self.get_household_structure()})
