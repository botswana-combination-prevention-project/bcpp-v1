import re

from apps.bcpp_clinic.models import ClinicConsent, ClinicVisit, ClinicSubjectLocator, ClinicEligibility
from apps.bcpp_lab.models import ClinicRequisition, PackingList

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject


class ClinicDashboard(RegisteredSubjectDashboard):

    view = 'clinic_dashboard'

    def __init__(self, *args, **kwargs):
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.dashboard_type_list = ['clinic']
        kwargs.update({'dashboard_models': {'clinic_eligibility': ClinicEligibility}, 'membership_form_category': 'consenting'})
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

    @property
    def registered_subject(self):
        return self._registered_subject

    @registered_subject.setter
    def registered_subject(self, pk=None):
        self._registered_subject = None
        print self.dashboard_id
        self.set_registered_subject(pk)
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not self._registered_subject:
            if not self._registered_subject and self.dashboard_model == RegisteredSubject or self.dashboard_model == ClinicEligibility:
                try:
                    self._registered_subject = RegisteredSubject.objects.get(registration_identifier=self.dashboard_id)
                except RegisteredSubject.DoesNotExist:
                    try:
                        self._registered_subject = RegisteredSubject.objects.get(pk=self.dashboard_id)
                    except RegisteredSubject.DoesNotExist:
                        pass
            elif not self._registered_subject and 'get_registered_subject' in dir(self.dashboard_model):
                self._registered_subject = self.dashboard_model_instance.registered_subject
            elif not self._registered_subject and re_pk.match(str(pk)):
                self._registered_subject = RegisteredSubject.objects.get(pk=pk)
            elif not self._registered_subject and self.appointment:
                # can i get it from an appointment? TODO: is this even possible?
                self._registered_subject = self.appointment.registered_subject
            elif self._registered_subject:
                if not isinstance(self._registered_subject, RegisteredSubject):
                    raise TypeError('Expected instance of RegisteredSubject. See {0}'.format(self))
            else:
                pass
        if not self._registered_subject:
            raise TypeError('Attribute \'_registered_subject\' may not be None. Perhaps add method registered_subject to the model {0}. See {1}'.format(self.dashboard_model, self))
