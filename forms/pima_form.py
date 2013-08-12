from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Pima


class PimaForm (BaseSubjectModelForm):

    class Meta:
        model = Pima
