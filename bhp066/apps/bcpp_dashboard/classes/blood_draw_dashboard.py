from django.template.loader import render_to_string
from apps.bcpp_rbd.models import RBDLocator, RBDVisit
from apps.bcpp_rbd.models import RBDConsent
from apps.bcpp_subject.models import SubjectReferral
from base_subject_dashboard import BaseSubjectDashboard
from apps.bcpp_lab.models import RBDRequisition, PackingList


class BloodDrawDashboard(BaseSubjectDashboard):

    view = 'rbd_dashboard'
    dashboard_name = 'Participant Dashboard'

    def __init__(self, **kwargs):
        #self.dashboard_type = 'rbd_subject'
        #kwargs.update({'dashboard_models': {'subject_consent_rbd': SubjectConsentRbd}})
        self.household_dashboard_url = 'household_dashboard_url'
        self.dashboard_type_list = ['rbd_subject']
        self.form_category = 'subject_rbd-year-1'
        kwargs.update({'dashboard_models': {'subject_consent': RBDConsent}})
        self.visit_model = RBDVisit
        super(BloodDrawDashboard, self).__init__(**kwargs)

    def add_to_context(self):
        super(BloodDrawDashboard, self).add_to_context()
        self.context.add(
            home='bcpp',
            search_name='subject',
            household_dashboard_url=self.household_dashboard_url,
            title='Research Blood Draw Dashboard',
            subject_consent=self.consent,
            subject_referral=self.subject_referral,
            rendered_household_members_sidebar=self.render_household_members_sidebar(),
            )

    @property
    def consent(self):
        """Returns to the subject consent, if it has been completed."""
        self._consent = None
        if RBDConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = RBDConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    @property
    def subject_referral(self):
        if SubjectReferral.objects.filter(subject_visit=self.visit_model_instance):
            return SubjectReferral.objects.get(subject_visit=self.visit_model_instance)
        return 'unknown referral'

    @property
    def requisition_model(self):
        return RBDRequisition

    @property
    def locator_model(self):
        return RBDLocator

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
