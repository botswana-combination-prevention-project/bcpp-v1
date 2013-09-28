from bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry
from base_membership_form import BaseMembershipForm


class SubjectAbsenteeEntryForm(BaseMembershipForm):

    household_member_fk = 'subject_absentee'

    class Meta:
        model = SubjectAbsenteeEntry


class SubjectAbsenteeForm(BaseMembershipForm):

    class Meta:
        model = SubjectAbsentee
