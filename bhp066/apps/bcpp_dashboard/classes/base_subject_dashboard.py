import re

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject
from edc.subject.appointment.models import Appointment

from apps.bcpp_household_member.models import HouseholdMember


class BaseSubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self, *args, **kwargs):

        dashboard_models = kwargs.get('dashboard_models', {})
        dashboard_models.update({'household_member': HouseholdMember})
        kwargs.update({'dashboard_models': dashboard_models})
        self.household_member = (kwargs.get('dashboard_model'), kwargs.get('dashboard_id'))
        if not self.form_category:
            self.form_category = self.survey.survey_slug
        kwargs.update({'membership_form_category': self.form_category})

        super(BaseSubjectDashboard, self).__init__(*args, **kwargs)

        self.extra_url_context = '&household_member={0}'.format(self.household_member.pk)

    def add_to_context(self):
        super(BaseSubjectDashboard, self).add_to_context()
        self.context.add(
            home='bcpp_survey',
            search_name='subject',
            title='Subject Dashboard',
            household_dashboard_url='household_dashboard_url',
            household_member=self.household_member,
            subject_consent=self.consent,
            household=self.household,
            survey=self.survey,
            household_members=self.household_members,
            household_structure=self.household_member.household_structure,
            )

    @property
    def survey(self):
        return self.household_member.survey

    @property
    def household_member(self):
        return self._household_member

    @household_member.setter
    def household_member(self, (dashboard_model_name, dashboard_id)):
        self._household_member = None
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(dashboard_id or ''):
            if dashboard_model_name == 'household_member':
                self._household_member = HouseholdMember.objects.get(pk=dashboard_id)
            elif dashboard_model_name == 'visit':
                self._household_member = self.visit_model.objects.get(pk=dashboard_id).household_member
            elif dashboard_model_name == 'appointment':
                appointment = Appointment.objects.get(pk=dashboard_id)
                # TODO: should I set appointment now?
                self._household_member = HouseholdMember.objects.filter(registered_subject=appointment.registered_subject).order_by('-created')[0]
            elif dashboard_model_name == 'registered_subject':
                # may have more than on, so take most recent
                self._household_member = HouseholdMember.objects.filter(registered_subject=dashboard_id).order_by('-created')[0]
        if not self._household_member:
            raise TypeError('Attribute _household_member may not be None. Using dashboard_model={0}, dashboard_id={1}'.format(dashboard_model_name, dashboard_id))

    @property
    def household(self):
        return self.household_structure.household

    @property
    def household_structure(self):
        return self.household_member.household_structure

    @property
    def registered_subject(self, pk=None):
        return self._registered_subject

    @registered_subject.setter
    def registered_subject(self, pk=None):
        """Sets the registered subject using a given pk or from household member."""
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self._registered_subject = None
        if re_pk.match(str(pk)):
            self._registered_subject = RegisteredSubject.objects.get(pk=pk)
        elif RegisteredSubject.objects.filter(registration_identifier=self.household_member.internal_identifier).exists():
            self._registered_subject = RegisteredSubject.objects.get(registration_identifier=self.household_member.internal_identifier)
        elif self.appointment:
            self._registered_subject = self.appointment.registered_subject
        else:
            raise ValueError('Expect all household_members to have an entry in RegisterSubject. Got None for member {0}.'.format(self.household_member))

    @property
    def household_members(self):
        return HouseholdMember.objects.filter(
            household_structure=self.household_member.household_structure).order_by('household_structure', 'first_name')
