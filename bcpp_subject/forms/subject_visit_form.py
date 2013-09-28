from edc_lib.bhp_consent.forms import BaseConsentedModelForm
from bcpp_subject.models import SubjectVisit


class SubjectVisitForm (BaseConsentedModelForm):

    class Meta:
        model = SubjectVisit
