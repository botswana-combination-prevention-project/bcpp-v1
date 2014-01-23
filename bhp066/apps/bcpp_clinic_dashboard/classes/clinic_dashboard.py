from apps.bcpp_clinic.models import ClinicConsent, ClinicVisit
from apps.bcpp_clinic_lab.models import ClinicRequisition, ClinicPackingList

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject
# from edc.subject.visit_schedule.models import MembershipForm


class ClinicDashboard(RegisteredSubjectDashboard):

    view = 'clinic_dashboard'

    def __init__(self, *args, **kwargs):
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.dashboard_type_list = ['clinic']
        kwargs.update({'dashboard_models': {'clinic_consent': ClinicConsent}, 'membership_form_category': 'clinic'})
        self.visit_model = ClinicVisit
        self._locator_model = None
        self._registered_subject = None
        self.extra_url_context = ""
        super(ClinicDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(ClinicDashboard, self).add_to_context()
        self.context.add(
            home='clinic',
            search_name='clinic',
            subject_dashboard_url=self.subject_dashboard_url,
            title='Clinic Participant Dashboard',
            clinic_consent=self.consent,
            )

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        self._consent = None
        if ClinicConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = ClinicConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    def set_registered_subject(self, pk=None):
        self._registered_subject = self.registered_subject
        if RegisteredSubject.objects.filter(subject_identifier=self.subject_identifier):
            self._registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
            #self.registered_subject = self._registered_subject

    def get_registered_subject(self):
        if not self._registered_subject:
            self.set_registered_subject()
        return self._registered_subject

    def set_membership_form_category(self):
        self._membership_form_category = self.membership_form_category
        self._membership_form_category = 'clinic'
        return self._membership_form_category

    @property
    def requisition_model(self):
        return ClinicRequisition

    @property
    def packing_list_model(self):
        return ClinicPackingList

    def render_labs(self, update=False):
        return ''
