from django import forms
from bcpp_household.models import ContactLogItem


class ContactLogItemForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('is_contacted').lower() == 'no' and (cleaned_data.get('information_provider') or cleaned_data.get('subject_status')):
            raise forms.ValidationError('You wrote contact was NOT made yet have recorded either the information provider or subject_status. Please correct.')
        if cleaned_data.get('is_contacted').lower() == 'yes' and (not cleaned_data.get('information_provider') or not cleaned_data.get('subject_status')):
            raise forms.ValidationError('You wrote contact was made. Please indicate the information provider and subject_status. Please correct.')

        return cleaned_data

    class Meta:
        model = ContactLogItem
