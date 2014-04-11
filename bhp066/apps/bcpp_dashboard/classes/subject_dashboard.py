from django.template.loader import render_to_string

from apps.bcpp_subject.models import SubjectConsent, SubjectVisit, SubjectLocator, SubjectReferral
from apps.bcpp_lab.models import SubjectRequisition, PackingList


from .base_subject_dashboard import BaseSubjectDashboard


class SubjectDashboard(BaseSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_name = 'Participant Dashboard'

    def __init__(self, *args, **kwargs):
        self.household_dashboard_url = 'household_dashboard_url'
        self.dashboard_type_list = ['subject']
        self.form_category = None
        kwargs.update({'dashboard_models': {'subject_consent': SubjectConsent}})
        self.visit_model = SubjectVisit
        super(SubjectDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(SubjectDashboard, self).add_to_context()
        self.context.add(
            home='bcpp',
            search_name='subject',
            household_dashboard_url=self.household_dashboard_url,
            title='Research Subject Dashboard',
            subject_consent=self.consent,
            subject_referral=self.subject_referral,
            rendered_household_members_sidebar=self.render_household_members_sidebar(),
            )

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        try:
            subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        except SubjectConsent.DoesNotExist:
            subject_consent = None
        return subject_consent

    @property
    def subject_referral(self):
        try:
            subject_referral = SubjectReferral.objects.get(subject_visit__household_member=self.household_member)
        except SubjectReferral.DoesNotExist:
            subject_referral = None
        return subject_referral

    @property
    def requisition_model(self):
        return SubjectRequisition

    @property
    def locator_model(self):
        return SubjectLocator

    @property
    def locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000'

    @property
    def packing_list_model(self):
        return PackingList

    def render_labs(self, update=False):
        return ''

    def render_household_members_sidebar(self):
        """Renders to string the household members sidebar."""
        return render_to_string('household_members_sidebar.html',
            {'household_members': self.household_members,
             'household_dashboard_url': self.household_dashboard_url,
             'household_structure': self.household_structure})
