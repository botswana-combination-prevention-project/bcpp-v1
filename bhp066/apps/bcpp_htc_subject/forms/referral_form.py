from django import forms
from ..models import Referral
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class ReferralForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(ReferralForm, self).clean()
        referred_for = cleaned_data.get("referred_for")
        # validate referral to
        if referred_for is not None:
            raise forms.ValidationError("Please indicate where the participant is referred to.")

        return cleaned_data

    class Meta:
        model = Referral
