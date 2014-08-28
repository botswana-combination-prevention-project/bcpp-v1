from django.forms import ValidationError

from edc.base.form.forms import BaseModelForm

from ..models import CorrectConsent


class CorrectConsentForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.instance.compare_old_fields_to_consent(CorrectConsent(**cleaned_data), ValidationError)
        return cleaned_data

    class Meta:
        model = CorrectConsent