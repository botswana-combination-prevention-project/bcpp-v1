from edc.subject.appointment.models import Appointment

from apps.bcpp_clinic.models import ClinicConsent, ClinicVisit, ClinicSubjectLocator, ClinicEligibility
from apps.bcpp_lab.models import ClinicRequisition, PackingList

from .base_subject_dashboard import BaseSubjectDashboard


class ClinicDashboard(BaseSubjectDashboard):

    view = 'clinic_dashboard'
    dashboard_url_name = 'clinic_dashboard_url'
    # dashboard_name = 'Clinic Participant Dashboard'

    def __init__(self, *args, **kwargs):
        self.subject_dashboard_url = 'clinic_dashboard_url'
        self.dashboard_type_list = ['clinic']
        kwargs.update({'dashboard_models': {'clinic_eligibility': ClinicEligibility},
                       'membership_form_category': 'bcpp_clinic',
                       })
        self._registered_subject = None
        self.form_category = 'bcpp_clinic'
        self._requisition_model = ClinicRequisition
        self.visit_model = ClinicVisit
        self._locator_model = ClinicSubjectLocator
        self.extra_url_context = ""
        super(ClinicDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(BaseSubjectDashboard, self).add_to_context()
        self.context.add(
            home='clinic',
            search_name='clinic',
            subject_dashboard_url=self.subject_dashboard_url,
            title='Clinic Subject Dashboard',
            subject_consent=self.consent,
            household_member=self.household_member,
            )

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        self._consent = None
        if ClinicConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = ClinicConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    def set_membership_form_category(self):
        self._membership_form_category = self.membership_form_category
        self._membership_form_category = 'bcpp_clinic'
        return self._membership_form_category

    def subject_hiv_status(self):
        return 'N/A'

    def render_subject_hiv_status(self):
        return ''

    @property
    def requisition_model(self):
        return ClinicRequisition

    @property
    def packing_list_model(self):
        return PackingList

    def render_labs(self, update=False):
        return ''

    @property
    def household_member(self):
        return self._household_member

    @household_member.setter
    def household_member(self, (dashboard_model_name, dashboard_id)):
        try:
            self._household_member = ClinicEligibility.objects.get(pk=dashboard_id).household_member
        except ClinicEligibility.DoesNotExist:
            try:
                self._household_member = ClinicVisit.objects.get(pk=dashboard_id).household_member
            except ClinicVisit.DoesNotExist:
                try:
                    appointment = Appointment.objects.get(pk=dashboard_id)
                    self._household_member = ClinicVisit.objects.get(appointment=appointment).household_member
                except Appointment.DoesNotExist:
                    raise TypeError('Attribute _household_member may not be None. Using dashboard_model={0}, '
                                    'dashboard_id={1}'.format(dashboard_model_name, dashboard_id))
