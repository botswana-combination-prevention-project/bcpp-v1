from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import HtcSubjectConsent


class HtcSubjectConsentForm(BaseConsentForm):

    class Meta:
        model = HtcSubjectConsent
