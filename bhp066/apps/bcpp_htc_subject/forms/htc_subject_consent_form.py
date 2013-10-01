from edc.subject.consent.forms import BaseSubjectConsentForm
from ..models import HtcSubjectConsent


class HtcSubjectConsentForm(BaseSubjectConsentForm):

    class Meta:
        model = HtcSubjectConsent
