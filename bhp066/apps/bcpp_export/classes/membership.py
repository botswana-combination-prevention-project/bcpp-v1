from apps.bcpp_household_member.models import HouseholdMember as HouseholdMemberModel


class Membership(object):
    """A class to store all household member records for a given internal identifier.

    Has two dictionaries to help refer to members by survey or member_status.

    Identifying fields like firstname, initials, ... are taken from the first
    occurrence of household member (chronological order)."""

    def __init__(self, household_member, survey_abbrevs):
        self.membership = []
        self.by_status = {}
        self.by_survey = {}
        self.internal_identifier = household_member.internal_identifier if household_member else None
        self.survey_abbrevs = survey_abbrevs
        for survey_abbrev in self.survey_abbrevs:
            try:
                hm = HouseholdMemberModel.objects.get(
                    internal_identifier=self.internal_identifier,
                    household_structure__survey__survey_abbrev=survey_abbrev)
                self.membership.append(hm)
                self.by_status.update({hm.member_status: hm})
                self.by_survey.update({survey_abbrev: hm})
            except HouseholdMemberModel.DoesNotExist:
                self.by_survey.update({survey_abbrev: None})
        attrs = [
            'first_name',
            'initials',
            'age_in_years',
            'gender',
            'study_resident']
        for attrname in attrs:
            setattr(self, attrname, self.first_attr_value(attrname))
        self.enumeration_first_date = self.first_attr_value('created').date() if self.membership else None
        self.enumeration_last_date = self.last_attr_value('created').date() if self.membership else None
        self.consented = True if [hm.is_consented for hm in self.membership if hm.is_consented] else None

    def first_attr_value(self, attrname):
        """Returns the value of attr from the first item in the list."""
        if not self.membership:
            return None
        return getattr(self.membership[0], attrname)

    def last_attr_value(self, attrname):
        """Returns the value of attr from the first item in the list."""
        if not self.membership:
            return None
        return getattr(self.membership[len(self.membership) - 1], attrname)

    def __repr__(self):
        return '{0}({1.internal_identifier!r}, {1.survey_abbrevs!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.internal_identifier!s, {1.survey_abbrevs!s}}'.format(self)
