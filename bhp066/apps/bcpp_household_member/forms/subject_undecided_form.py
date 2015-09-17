from ..models import SubjectUndecided, SubjectUndecidedEntry

from .base_membership_form import BaseMembershipForm


class SubjectUndecidedEntryForm(BaseMembershipForm):

    household_member_fk = 'subject_undecided'

    class Meta:
        model = SubjectUndecidedEntry


class SubjectUndecidedForm(BaseMembershipForm):

    class Meta:
        model = SubjectUndecided
