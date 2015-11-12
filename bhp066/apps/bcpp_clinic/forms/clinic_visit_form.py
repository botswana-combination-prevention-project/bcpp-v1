from edc_consent.forms import BaseSubjectConsentForm

from ..models import ClinicVisit


class ClinicVisitForm (BaseSubjectConsentForm):

    class Meta:
        model = ClinicVisit
