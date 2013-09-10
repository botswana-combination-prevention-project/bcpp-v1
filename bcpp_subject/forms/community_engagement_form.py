from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import CommunityEngagement


class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement
