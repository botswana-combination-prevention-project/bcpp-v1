from edc.subject.consent.forms import BaseConsentedModelForm

from ..models import SubjectVisit


class SubjectVisitForm (BaseConsentedModelForm):

    class Meta:
        model = SubjectVisit
