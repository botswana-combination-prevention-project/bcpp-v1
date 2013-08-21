from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import FollowupContactPermission


class FollowupContactPermissionForm (BaseHtcModelForm):

    class Meta:
        model = FollowupContactPermission
