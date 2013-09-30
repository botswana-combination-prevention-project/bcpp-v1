from django import forms
from ..models import HivTestingConsent
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class HivTestingConsentForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(HivTestingConsentForm, self).clean()
        testing_today = cleaned_data.get("testing_today")
        reason_not_testing = cleaned_data.get("reason_not_testing")
        # Ensure that if participant answered no the a reason is given
        if testing_today == 'No' and reason_not_testing is None:
            raise forms.ValidationError("Participant has answered \'No\' to testing"
                                        " please supply a reason.")
        # Ensure that if participant answered yes, then reason no testing is not filled
        if testing_today == 'Yes'and reason_not_testing is not None:
            raise forms.ValidationError("Participant has answered \'Yes\' to testing"
                                        " NO reason is required. Please correct.")

        return cleaned_data

    class Meta:
        model = HivTestingConsent
