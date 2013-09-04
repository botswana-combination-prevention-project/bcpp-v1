from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Stigma, StigmaOpinion, PositiveParticipant


class StigmaForm (BaseSubjectModelForm):

    class Meta:
        model = Stigma


class StigmaOpinionForm (BaseSubjectModelForm):

    class Meta:
        model = StigmaOpinion


class PositiveParticipantForm (BaseSubjectModelForm):

    class Meta:
        model = PositiveParticipant