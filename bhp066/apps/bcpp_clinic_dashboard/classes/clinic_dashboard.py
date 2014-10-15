from apps.bcpp_clinic.models import ClinicConsent, ClinicVisit, ClinicSubjectLocator, ClinicEligibility
from apps.bcpp_lab.models import ClinicRequisition, PackingList

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject


class ClinicDashboard(RegisteredSubjectDashboard):

    view = 'clinic_dashboard'

    def __init__(self, *args, **kwargs):
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.dashboard_type_list = ['subject']
        kwargs.update({'dashboard_models': {'clinic_consent': ClinicEligibility}, 'membership_form_category': 'clinic'})
        self._requisition_model = ClinicRequisition
        self.visit_model = ClinicVisit
        self._locator_model = ClinicSubjectLocator
        self._registered_subject = None
        self.extra_url_context = ""
        super(ClinicDashboard, self).__init__(*args, **kwargs)
#         self._locator_model = None
#         self._registered_subject = None
#         self.extra_url_context = ""
#         super(ClinicDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(ClinicDashboard, self).add_to_context()
        self.context.add(
            home='clinic',
            search_name='clinic',
            subject_dashboard_url=self.subject_dashboard_url,
            title='Clinic Subject Dashboard',
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
        self._membership_form_category = 'subject'
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
