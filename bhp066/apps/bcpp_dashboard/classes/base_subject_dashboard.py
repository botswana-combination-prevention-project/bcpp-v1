from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp_household_member.models import HouseholdMember


class BaseSubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self, **kwargs):
        super(BaseSubjectDashboard, self).__init__(**kwargs)
        self._household_member = None

    def get_context_data(self, **kwargs):
        self.context = super(BaseSubjectDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='bcpp_survey',
            search_name='subject',
            title=self.dashboard_name,
            household_dashboard_url='household_dashboard_url',
            household_member=self.household_member,
            # subject_consent=self.consent,
            household=self.household,
            survey=self.survey,
            household_members=self.household_members,
            household_structure=self.household_member.household_structure,
            membership_form_category=self.membership_form_category,
            extra_url_context='&household_member={0}'.format(self.household_member.pk),
        )
        return self.context

    @property
    def survey(self):
        return self.household_member.survey

    @property
    def household_member(self):
        if not self._household_member:
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

    @property
    def household(self):
        return self.household_member.household_structure.household

    @property
    def household_structure(self):
        return self.household_member.household_structure

    @property
    def registered_subject(self):
        if not self._registered_subject:
            try:
                self._registered_subject = RegisteredSubject.objects.get(
                    registration_identifier=self.household_member.internal_identifier)
            except RegisteredSubject.DoesNotExist:
                try:
                    self._registered_subject = RegisteredSubject.objects.get(pk=self.dashboard_id)
                except RegisteredSubject.DoesNotExist:
                    try:
                        self._registered_subject = self.appointment.registered_subject
                    except AttributeError:
                        pass
        return self._registered_subject

    @property
    def household_members(self):
        return HouseholdMember.objects.filter(
            household_structure=self.household_member.household_structure).order_by(
                'household_structure', 'first_name')
