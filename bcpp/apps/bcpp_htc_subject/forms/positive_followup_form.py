from django import forms
from ..models import PositiveFollowup
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class PositiveFollowupForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(PositiveFollowupForm, self).clean()
        contact_consent = cleaned_data.get("contact_consent")
        contact_family = cleaned_data.get("contact_family")

        if contact_consent == 'No' and contact_family is not None:
            raise forms.ValidationError("Participant did not give permission to follow up."
                                        "You cannot ask to contact family or friends. Please correct. ")

        if contact_consent == 'Yes' and contact_family is None:
            raise forms.ValidationError("Please indicate whether participant gives permission"
                                        " to contact family or friends")

        return cleaned_data

    class Meta:
        model = PositiveFollowup
