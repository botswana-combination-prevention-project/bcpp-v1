from ..models import RecentPartner, SecondPartner, ThirdPartner
from .base_subject_model_form import BaseSubjectModelForm


class RecentPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = RecentPartner


class SecondPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = SecondPartner


class ThirdPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = ThirdPartner
