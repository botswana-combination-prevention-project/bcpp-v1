from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household_member.models import HouseholdMember as HouseholdMemberModel
from apps.bcpp_export.classes.survey import Survey

from .base import Base
from .membership import Membership


class HouseholdMember(Base):
    """A wrapper class for Household Member."""
    def __init__(self, household_member, verbose=None):
        """Allows None for attribute inspection."""
        super(HouseholdMember, self).__init__(verbose=verbose)
        try:
            self.household_member = HouseholdMemberModel.objects.get(id=household_member)
        except HouseholdMemberModel.DoesNotExist:
            self.household_member = household_member
        if self.household_member:
            self.revision = self.household_member.revision
            self.household_structure = self.household_member.household_structure
            self.household = self.household_member.household_structure.household
            self.household_identifier = self.household.household_identifier
            self.community = self.household.plot.community
        else:
            self.revision = None
            self.household_structure = None
            self.household = None
            self.household_identifier = None
            self.community = None
        try:
            self.internal_identifier = self.household_member.internal_identifier
        except AttributeError:
            self.internal_identifier = None
        self.survey = Survey(self.community, verbose=self.verbose)
        self.membership = Membership(self.household_member, self.survey.survey_abbrevs)
        try:
            self.registered_subject = RegisteredSubject.objects.get(
                registration_identifier=self.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            self.registered_subject = None

    def __repr__(self):
        return '{0}({1.household_member!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.household_member!s}'.format(self)
