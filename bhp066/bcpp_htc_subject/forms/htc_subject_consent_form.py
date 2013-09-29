from bhp_consent.forms import BaseSubjectConsentForm
from ..models import HtcSubjectConsent


class HtcSubjectConsentForm(BaseSubjectConsentForm):

    class Meta:
        model = HtcSubjectConsent
