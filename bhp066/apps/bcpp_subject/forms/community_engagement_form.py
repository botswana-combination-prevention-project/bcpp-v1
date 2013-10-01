from ..models import CommunityEngagement
from .base_subject_model_form import BaseSubjectModelForm


class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement
