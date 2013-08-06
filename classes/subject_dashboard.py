import re
from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bhp_registration.models import RegisteredSubject
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectVisit
from bcpp_lab.models import SubjectRequisition, PackingList


class SubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self):
        super(SubjectDashboard, self).__init__()
        self._survey = None
        self._household_member = None
        self._household_members = None
        self._household = None

        self.exclude_others_if_keyed_model_name = 'subjectconsent'

        self.context.add(
            home='bcpp_survey',
            search_name='subject',
            household_dashboard_url='household_dashboard_url',
            subject_dashboard_url='subject_dashboard_url',
            subject_dashboard_visit_url='subject_dashboard_visit_url',
            )

    def create(self, **kwargs):
        super(SubjectDashboard, self).create(**kwargs)
        self.context.add(
            household_member=self.get_household_member(),
            subject_consent=self.get_household_member().consent(),
            household=self.get_household(),
            survey=self.get_survey(),
            title='Subject Dashboard',
            household_members=self.get_household_members(),
            household_structure=self.get_household_member().household_structure,
            )

    def set_dashboard_model_reference(self):
        """Returns a dictionary of format { 'model_name': ('app_label', 'model_name')} or { 'model_name': Model}.

        Users should override to add more to the dictionary than the default."""
        super(SubjectDashboard, self).set_dashboard_model_reference()
        self._dashboard_model_reference.update({'household_member': HouseholdMember})

    def set_extra_url_context(self, value=None):
        self._extra_url_context = '&household_member={0}'.format(self.get_household_member().pk)

    def set_membership_form_category(self):
        self._membership_form_category = (self.get_survey().survey_slug)

    def set_visit_model(self):
        if self.get_dashboard_type() == 'subject':
            self._visit_model = SubjectVisit

    def set_requisition_model(self):
        if self.get_dashboard_type() == 'subject':
            self._requisition_model = SubjectRequisition

    def set_packing_list_model(self):
        if self.get_dashboard_type() == 'subject':
            self._packing_list_model = PackingList

    def get_dashboard_model_reference(self):
        """Returns a dictionary of format { 'model_name': ('app_label', 'model_name')} or { 'model_name': Model}."""
        return {'household_member': HouseholdMember}

    def set_survey(self):
        self._survey = self.get_household_member().survey

    def get_survey(self):
        if not self._survey:
            self.set_survey()
        return self._survey

    def set_household_member(self):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(self.get_dashboard_id() or ''):
            if self.get_dashboard_model_key() == 'household_member':
                self._household_member = HouseholdMember.objects.get(pk=self.get_dashboard_id())
            if self.get_dashboard_model_key() == 'visit':
                self._household_member = self.get_visit_model().objects.get(pk=self.get_dashboard_id()).household_member
            if self.get_dashboard_model_key() == 'appointment':
                if self.get_visit_model_instance():
                    self._household_member = self.get_visit_model_instance().household_member
                elif self.get_appointment():
                    # may have more than on, so take most recent
                    self._household_member = HouseholdMember.objects.filter(registered_subject=self.get_appointment().registered_subject).order_by('-created')[0]
                else:
                    pass
            if self.get_dashboard_model_key() == 'registered_subject':
                # may have more than on, so take most recent
                self._household_member = HouseholdMember.objects.filter(registered_subject=self.get_dashboard_id()).order_by('-created')[0]
        if not self._household_member:
            raise TypeError('Attribute _household_member may not be None. Using dashboard_model={0}, dashboard_id={1}'.format(self.get_dashboard_model(), self.get_dashboard_id()))

    def get_household_member(self):
        if not self._household_member:
            self.set_household_member()
        return self._household_member

    def set_household(self):
        self._household = self.get_household_member().household

    def get_household(self):
        if not self._household:
            self.set_household()
        return self._household

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
