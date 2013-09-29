from bhp_consent.forms import BaseConsentedModelForm
from bcpp_htc_subject.models import HtcSubjectVisit


class HtcVisitForm (BaseConsentedModelForm):

    class Meta:
        model = HtcSubjectVisit
