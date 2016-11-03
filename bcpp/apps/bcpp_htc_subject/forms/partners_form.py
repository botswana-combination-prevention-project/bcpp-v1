from ..models import HtcRecentPartner, HtcSecondPartner, HtcThirdPartner
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class HtcRecentPartnerForm (BaseHtcScheduledModelForm):

    class Meta:
        model = HtcRecentPartner


class HtcSecondPartnerForm (BaseHtcScheduledModelForm):

    class Meta:
        model = HtcSecondPartner


class HtcThirdPartnerForm (BaseHtcScheduledModelForm):

    class Meta:
        model = HtcThirdPartner
