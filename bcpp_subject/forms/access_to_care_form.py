from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import AccessToCare


class AccessToCareForm (BaseSubjectModelForm):

    class Meta:
        model = AccessToCare
