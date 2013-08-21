# from bhp_consent.forms import BaseConsentedModelForm
from bhp_base_form.forms import BaseModelForm
from bcpp_htc.models import HtcVisit


class BaseHtcModelForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseHtcModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['htc_visit'].queryset = HtcVisit.objects.filter(pk=self.instance.htc_visit.pk)
        except:
            pass
