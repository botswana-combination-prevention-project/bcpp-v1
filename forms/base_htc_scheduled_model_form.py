# from bhp_consent.forms import BaseConsentedModelForm
from bhp_base_form.forms import BaseModelForm
from bcpp_htc_subject.models import HtcSubjectVisit


class BaseHtcScheduledModelForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseHtcScheduledModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['htc_subject_visit'].queryset = HtcSubjectVisit.objects.filter(pk=self.instance.htc_visit.pk)
        except:
            pass
