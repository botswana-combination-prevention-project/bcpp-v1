from base_membership_form import BaseMembershipForm
from bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry


class SubjectAbsenteeEntryForm(BaseMembershipForm):

    household_structure_member_fk = 'subject_absentee'

    class Meta:
        model = SubjectAbsenteeEntry


class SubjectAbsenteeForm(BaseMembershipForm):

    class Meta:
        model = SubjectAbsentee
