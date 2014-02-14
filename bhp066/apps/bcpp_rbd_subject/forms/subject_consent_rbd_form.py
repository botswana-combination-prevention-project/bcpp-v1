from apps.bcpp_subject.forms import MainConsentForm
from apps.bcpp_rbd_subject.models import SubjectConsentRBDonly

class SubjectConsentRBDForm(MainConsentForm):

    class Meta:
        model = SubjectConsentRBDonly
