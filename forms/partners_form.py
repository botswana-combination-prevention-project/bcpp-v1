from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import RecentPartner, SecondPartner, ThirdPartner


class RecentPartnerForm (BaseHtcModelForm):

    class Meta:
        model = RecentPartner


class SecondPartnerForm (BaseHtcModelForm):

    class Meta:
        model = SecondPartner


class ThirdPartnerForm (BaseHtcModelForm):

    class Meta:
        model = ThirdPartner
