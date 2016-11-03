from bhp066.apps.bcpp_clinic.models import ClinicConsent, ClinicVisit, ClinicSubjectLocator, ClinicEligibility
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_lab.models import ClinicRequisition, PackingList

from .base_subject_dashboard import BaseSubjectDashboard


class ClinicDashboard(BaseSubjectDashboard):

    view = 'clinic_dashboard'
    dashboard_url_name = 'clinic_dashboard_url'
    dashboard_name = 'Clinic Participant Dashboard'
    urlpattern_view = 'apps.bcpp_dashboard.views'
    template_name = 'clinic_dashboard.html'
    base_subject_urls = BaseSubjectDashboard.urlpatterns
    urlpatterns = [
        BaseSubjectDashboard.urlpatterns[0][:-1] + '(?P<appointment_code>{appointment_code})/$'] + base_subject_urls
    urlpattern_options = dict(
        BaseSubjectDashboard.urlpattern_options,
        dashboard_model=BaseSubjectDashboard.urlpattern_options['dashboard_model'] + '|clinic_eligibility',
        dashboard_type='clinic',
        appointment_code='T0|T1|T2|T3|T4')

    def __init__(self, **kwargs):
        super(ClinicDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'clinic_dashboard_url'
        self.membership_form_category = ['bcpp_clinic']
        self.dashboard_type_list = ['clinic']
        self.requisition_model = ClinicRequisition
        self.visit_model = ClinicVisit
        self._locator_model = ClinicSubjectLocator
        self.dashboard_models['clinic_eligibility'] = ClinicEligibility
        self.dashboard_models['clinic_consent'] = ClinicConsent
        self.dashboard_models['household_member'] = HouseholdMember
        self.dashboard_models['visit'] = self._visit_model
        # self.appointment_code = kwargs.get('visit_code')

    def get_context_data(self, **kwargs):
        super(BaseSubjectDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='clinic',
            search_name='clinic',
            subject_dashboard_url=self.subject_dashboard_url,
            title='Clinic Subject Dashboard',
            subject_consent=self.consent,
            clinic_consent=self.consent,
            household_member=self.household_member,
        )
        return self.context

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        self._consent = None
        if ClinicConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = ClinicConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    def subject_hiv_status(self):
        return 'N/A'

    def render_subject_hiv_status(self):
        return ''

    @property
    def packing_list_model(self):
        return PackingList

    def render_labs(self, update=False):
        return ''

    @property
    def household_member(self):
        if not self._household_member:
            try:
                self._household_member = ClinicEligibility.objects.get(pk=self.dashboard_id).household_member
            except ClinicEligibility.DoesNotExist:
                try:
                    self._household_member = HouseholdMember.objects.get(pk=self.dashboard_id)
                except HouseholdMember.DoesNotExist:
                    try:
                        self._household_member = self.visit_model.objects.get(pk=self.dashboard_id).household_member
                    except self.visit_model.DoesNotExist:
                        try:
                            self._household_member = self.visit_model.objects.get(
                                appointment=self.appointment).household_member
                        except self.visit_model.DoesNotExist:
                            pass
        return self._household_member
