from django import forms

from ..models import SubjectHtc

from edc.base.form.forms import BaseModelForm


class SubjectHtcForm(BaseModelForm):

    def clean(self):

        cleaned_data = super(SubjectHtcForm, self).clean()
        if cleaned_data.get('offered') == 'Yes':
            if cleaned_data.get('accepted') == 'Yes' and cleaned_data.get('refusal_reason'):
                raise forms.ValidationError('You wrote HTC was accepted. A refusal reason is not applicable.')
            if cleaned_data.get('accepted') == 'No' and not cleaned_data.get('refusal_reason'):
                raise forms.ValidationError('You wrote HTC was not accepted. A refusal reason is required.')
            if cleaned_data.get('referred') == 'N/A':
                raise forms.ValidationError('Please indicate whether the subject was referred.')
            if cleaned_data.get('referred') == 'Yes' and not cleaned_data.get('referral_clinic'):
                raise forms.ValidationError('Please indicate the referral clinic.')
            if cleaned_data.get('referred') == 'No' and cleaned_data.get('referral_clinic'):
                raise forms.ValidationError('Subject was not referred. The referral clinic is not applicable.')
            if cleaned_data.get('accepted') == 'Yes' and cleaned_data.get('hiv_result') == 'Declined':
                raise forms.ValidationError('You wrote subject accepted HTC but declined testing. Please correct.')

        else:
            if cleaned_data.get('accepted') != 'N/A':
                raise forms.ValidationError('HTC was not offered HTC. Whether subject accepted is not applicable.')
            if cleaned_data.get('refusal_reason'):
                raise forms.ValidationError('You wrote HTC was not offered. Refusal reason is not applicable.')
            if cleaned_data.get('referred') != 'N/A':
                raise forms.ValidationError('HTC was not offered HTC. Whether subject was referred is not applicable.')
            if cleaned_data.get('referral_clinic'):
                raise forms.ValidationError('HTC was not offered HTC. A referral clinic is not applicable.')
            if cleaned_data.get('hiv_result') != 'N/A':
                raise forms.ValidationError('HTC was not offered HTC. An HIV result is not applicable.')
        return cleaned_data

    class Meta:
        model = SubjectHtc
