# import re

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
# from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_clinic.models import ClinicConsent, ClinicVisit, ClinicSubjectLocator, ClinicEligibility
from apps.bcpp_lab.models import ClinicRequisition, PackingList


class ClinicDashboard(RegisteredSubjectDashboard):

    view = 'clinic_dashboard'

    def __init__(self, *args, **kwargs):
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.dashboard_type_list = ['clinic']
        kwargs.update({'dashboard_models': {'clinic_eligibility': ClinicEligibility},
                       'membership_form_category': 'consenting',
                       })
        self._registered_subject = None
        self._requisition_model = ClinicRequisition
        self.visit_model = ClinicVisit
        self._locator_model = ClinicSubjectLocator
        self.extra_url_context = ""
        super(ClinicDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(ClinicDashboard, self).add_to_context()
        self.context.add(
            home='clinic',
            search_name='clinic',
            subject_dashboard_url=self.subject_dashboard_url,
            title='Clinic Subject Dashboard',
            clinic_consent=self.consent,
            )

    def set_registered_subject(self, pk=None):
        # try:
        self._registered_subject = ClinicEligibility.objects.get(pk=self.dashboard_id).household_member.registered_subject
        # except ClinicEligibility.DoesNotExist:
        #    pass
        #    # self._registered_subject = RegisteredSubject.objects.get(pk=pk)

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        self._consent = None
        if ClinicConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = ClinicConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    def set_membership_form_category(self):
        self._membership_form_category = self.membership_form_category
        self._membership_form_category = 'consenting'
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
