from edc_consent.forms import BaseConsentedModelForm

from ..models import ClinicVisit


class ClinicVisitForm (BaseConsentedModelForm):

    class Meta:
        model = ClinicVisit
