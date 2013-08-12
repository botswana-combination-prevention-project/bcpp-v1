from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import NonPregnancy


class NonPregnancyForm (BaseSubjectModelForm):

    class Meta:
        model = NonPregnancy
