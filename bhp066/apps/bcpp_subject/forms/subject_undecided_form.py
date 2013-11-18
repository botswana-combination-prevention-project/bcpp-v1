from ..models import SubjectUndecided, SubjectUndecidedEntry
from bcpp_household_member.forms import BaseMembershipForm


class SubjectUndecidedEntryForm(BaseMembershipForm):

    household_member_fk = 'subject_undecided'

    class Meta:
        model = SubjectUndecidedEntry


class SubjectUndecidedForm(BaseMembershipForm):

    class Meta:
        model = SubjectUndecided
