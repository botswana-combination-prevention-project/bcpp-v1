from bcpp_subject.forms import BaseSubjectModelForm
from bcpp_htc.models import FollowupContactPermission


class FollowupContactPermissionForm (BaseSubjectModelForm):

    class Meta:
        model = FollowupContactPermission
