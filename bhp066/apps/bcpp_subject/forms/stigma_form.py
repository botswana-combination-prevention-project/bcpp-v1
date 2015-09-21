from ..models import Stigma, StigmaOpinion, PositiveParticipant

from .base_subject_model_form import BaseSubjectModelForm


class StigmaForm (BaseSubjectModelForm):

    class Meta:
        model = Stigma


class StigmaOpinionForm (BaseSubjectModelForm):

    class Meta:
        model = StigmaOpinion


class PositiveParticipantForm (BaseSubjectModelForm):

    class Meta:
        model = PositiveParticipant
