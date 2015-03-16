from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household_member.models import HouseholdMember as HouseholdMemberModel
from apps.bcpp_export.classes.survey import Survey

from .base import Base


class HouseholdMember(Base):

    def __init__(self, household_member, verbose=None):
        super(HouseholdMember, self).__init__(verbose=verbose)
        self.household_member = household_member
        self.household_structure = self.household_member.household_structure if self.household_member else None
        self.household_identifier = self.household_member.household_structure.household.household_identifier
        self.community = self.household_member.household_structure.household.plot.community
        try:
            self.internal_identifier = self.household_member.internal_identifier
        except AttributeError:
            self.internal_identifier = None
        self.membership = []
        self.membership_by_status = {}
        self.membership_by_survey = {}
        self.survey = Survey(self.community, verbose=self.verbose)
        for survey_abbrev in self.survey.survey_abbrevs:
            try:
                hm = HouseholdMemberModel.objects.get(
                    internal_identifier=self.internal_identifier,
                    household_structure__survey__survey_abbrev=survey_abbrev)
                self.membership.append(hm)
                self.membership_by_status.update({hm.member_status: hm})
                self.membership_by_survey.update({survey_abbrev: hm})
            except HouseholdMemberModel.DoesNotExist:
                self.membership_by_survey.update({survey_abbrev: None})
        try:
            self.registered_subject = RegisteredSubject.objects.get(
                registration_identifier=self.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            self.registered_subject = None
        self.first_name = self.membership[0].first_name if self.membership else None
        self.initials = self.membership[0].initials if self.membership else None
        self.age_in_years = self.membership[0].age_in_years if self.membership else None
        self.gender = self.membership[0].gender if self.membership else None
        self.study_resident = self.membership[0].study_resident if self.membership else None
        self.enumeration_first_date = self.membership[0].created.date() if self.membership else None
        self.enumeration_last_date = self.membership[len(self.membership) - 1].created.date() if self.membership else None
        self.consented = True if [hm.is_consented for hm in self.membership if hm.is_consented] else None

    def __repr__(self):
        return '{0}({1.household_member!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.household_member!s}'.format(self)
