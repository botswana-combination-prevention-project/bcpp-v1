import re
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject
from apps.bcpp_household_member.models import HouseholdMember


class BaseSubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self, *args, **kwargs):
        self._survey = None
        self._household_member = None
        self._household_members = None
        self._household = None
        self._household_structure = None
        dashboard_models = kwargs.get('dashboard_models', {})
        dashboard_models.update({'household_member': HouseholdMember})
        kwargs.update({'dashboard_models': dashboard_models})
        super(BaseSubjectDashboard, self).__init__(*args, **kwargs)

    def add_to_context(self):
        super(BaseSubjectDashboard, self).add_to_context()
        self.context.add(
            home='bcpp_survey',
            search_name='subject',
            title='Subject Dashboard',
            household_dashboard_url='household_dashboard_url',
            household_member=self.get_household_member(),
            subject_consent=self.get_household_member().consent(),
            household=self.get_household(),
            survey=self.get_survey(),
            household_members=self.get_household_members(),
            household_structure=self.get_household_member().household_structure,
            )

    def set_extra_url_context(self, value=None):
        self._extra_url_context = '&household_member={0}'.format(self.get_household_member().pk)

    def set_membership_form_category(self):
        self._membership_form_category = (self.get_survey().survey_slug)

    def set_survey(self):
        self._survey = self.get_household_member().survey

    def get_survey(self):
        if not self._survey:
            self.set_survey()
        return self._survey

    def set_household_member(self):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(self.get_dashboard_id() or ''):
            if self.get_dashboard_model_name() == 'household_member':
                self._household_member = HouseholdMember.objects.get(pk=self.get_dashboard_id())
            if self.get_dashboard_model_name() == 'visit':
                self._household_member = self.get_visit_model().objects.get(pk=self.get_dashboard_id()).household_member
            if self.get_dashboard_model_name() == 'appointment':
                if self._get_visit_model_instance():
                    self._household_member = self._get_visit_model_instance().household_member
                elif self.get_appointment():
                    # may have more than on, so take most recent
                    self._household_member = HouseholdMember.objects.filter(registered_subject=self.get_appointment().registered_subject).order_by('-created')[0]
                else:
                    pass
            if self.get_dashboard_model_name() == 'registered_subject':
                # may have more than on, so take most recent
                self._household_member = HouseholdMember.objects.filter(registered_subject=self.get_dashboard_id()).order_by('-created')[0]
        if not self._household_member:
            raise TypeError('Attribute _household_member may not be None. Using dashboard_model={0}, dashboard_id={1}'.format(self.get_dashboard_model(), self.get_dashboard_id()))

    def get_household_member(self):
        if not self._household_member:
            self.set_household_member()
        return self._household_member

    def set_household(self):
        self._household = self.get_household_structure().household

    def get_household(self):
        if not self._household:
            self.set_household()
        return self._household

    def set_household_structure(self):
        self._household_structure = self.get_household_member().household_structure

    def get_household_structure(self):
        if not self._household_structure:
            self.set_household_structure()
        return self._household_structure

    def set_registered_subject(self, value=None):
        """Sets the registered subject using a given pk or from household member."""
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self._registered_subject = None
        if re_pk.match(str(value)):
            self._registered_subject = RegisteredSubject.objects.get(pk=value)
        elif self.get_appointment():
            self._registered_subject = self.get_appointment().registered_subject
        elif RegisteredSubject.objects.filter(registration_identifier=self.get_household_member().internal_identifier).exists():
            self._registered_subject = RegisteredSubject.objects.get(registration_identifier=self.get_household_member().internal_identifier)
        else:
            raise ValueError('Expect all household_members to have an entry in RegisterSubject. Got None for member {0}.'.format(self.get_household_member()))

    def set_household_members(self):
        self._household_members = HouseholdMember.objects.filter(
            household_structure=self.get_household_member().household_structure).order_by('household_structure', 'first_name')

    def get_household_members(self):
        if not self._household_members:
            self.set_household_members()
        return self._household_members
