from bhp_consent.forms import BaseConsentedModelForm
from bcpp_htc.models import HtcVisit


class HtcVisitForm (BaseConsentedModelForm):

    class Meta:
        model = HtcVisit
