from edc.subject.consent.forms import BaseConsentedModelForm
from ..models import HtcSubjectVisit


class HtcVisitForm (BaseConsentedModelForm):

    class Meta:
        model = HtcSubjectVisit
