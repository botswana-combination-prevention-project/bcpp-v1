from base_membership_form import BaseMembershipForm
from bcpp_subject.models import SubjectUndecided, SubjectUndecidedEntry


class SubjectUndecidedEntryForm(BaseMembershipForm):

    household_member_fk = 'subject_undecided'

    class Meta:
        model = SubjectUndecidedEntry


class SubjectUndecidedForm(BaseMembershipForm):

    class Meta:
        model = SubjectUndecided
