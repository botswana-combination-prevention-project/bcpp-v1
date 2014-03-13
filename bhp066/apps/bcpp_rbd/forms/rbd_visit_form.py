from edc.subject.consent.forms import BaseConsentedModelForm

from ..models import RBDVisit


class RBDVisitForm(BaseConsentedModelForm):

    class Meta:
        model = RBDVisit
