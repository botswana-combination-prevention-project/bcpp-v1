from edc.core.bhp_consent.forms import BaseConsentedModelForm
from ..models import SubjectVisit


class BaseSubjectModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseSubjectModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject_visit'].queryset = SubjectVisit.objects.filter(pk=self.instance.subject_visit.pk)
        except:
            pass
