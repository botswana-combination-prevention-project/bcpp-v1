from bhp_consent.forms import BaseConsentedModelForm
from bcpp_subject.models import SubjectVisit


class BaseSubjectModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseSubjectModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject_visit'].queryset = SubjectVisit.objects.filter(pk=self.instance.subjectvisit.pk)
        except:
            pass
