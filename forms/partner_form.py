from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import RecentPartner, SecondPartner, ThirdPartner


class RecentPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = RecentPartner


class SecondPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = SecondPartner


class ThirdPartnerForm (BaseSubjectModelForm):

    class Meta:
        model = ThirdPartner
