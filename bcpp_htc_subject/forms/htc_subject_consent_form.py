from bhp_consent.forms import BaseSubjectConsentForm
from bcpp_htc_subject.models import HtcSubjectConsent


class HtcSubjectConsentForm(BaseSubjectConsentForm):

    class Meta:
        model = HtcSubjectConsent
