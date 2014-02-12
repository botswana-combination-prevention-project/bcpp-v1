from edc.subject.consent.forms import BaseConsentedModelForm
from apps.bcpp_rbd_subject.models import SubjectVisitRBD


class SubjectVisitRBDForm(BaseConsentedModelForm):

    class Meta:
        model = SubjectVisitRBD