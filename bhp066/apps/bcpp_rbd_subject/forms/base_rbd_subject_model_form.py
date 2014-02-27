from edc.subject.consent.forms import BaseConsentedModelForm
from ..models import SubjectVisitRBD


class BaseRBDSubjectModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseRBDSubjectModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject_visit'].queryset = SubjectVisitRBD.objects.filter(pk=self.instance.subject_visit_rbd.pk)
        except:
            pass
