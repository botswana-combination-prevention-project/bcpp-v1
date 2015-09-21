from edc_consent.forms import BaseConsentedModelForm

from ..models import ClinicVisit


class BaseClinicModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseClinicModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['clinic_visit'].queryset = ClinicVisit.objects.filter(pk=self.instance.clinic_visit.pk)
        except:
            pass
