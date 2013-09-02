# from bhp_consent.forms import BaseConsentedModelForm
from bhp_base_form.forms import BaseModelForm
from bcpp_subject_htc.models import HtcSubjectVisit


class BaseHtcModelForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseHtcModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['htc_subject_visit'].queryset = HtcSubjectVisit.objects.filter(pk=self.instance.htc_visit.pk)
        except:
            pass
