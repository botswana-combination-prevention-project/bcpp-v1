from ..models import Participation

from .base_subject_model_form import BaseSubjectModelForm


class ParticipationForm (BaseSubjectModelForm):

    class Meta:
        model = Participation
