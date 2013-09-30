from django import forms
from ..models import HtcHivResult
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class HtcHivResultForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(HtcHivResultForm).clean()
        couples_testing = cleaned_data.get("couples_testing")
        partner_id = cleaned_data.get("partner_id")

        if couples_testing == 'Yes' and partner_id is None:
            raise forms.ValidationError("Partner unique identifier required.")

        return cleaned_data

    class Meta:
        model = HtcHivResult
