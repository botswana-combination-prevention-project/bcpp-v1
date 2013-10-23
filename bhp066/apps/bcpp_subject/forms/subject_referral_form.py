from ..models import SubjectReferral
from .base_subject_model_form import BaseSubjectModelForm


class SubjectReferralForm(BaseSubjectModelForm):

    class Meta:
        model = SubjectReferral
