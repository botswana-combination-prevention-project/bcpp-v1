from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import HtcSubjectVisit


class BaseHtcScheduledModelForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseHtcScheduledModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['htc_subject_visit'].queryset = HtcSubjectVisit.objects.filter(pk=self.instance.htc_visit.pk)
        except AttributeError:
            pass
