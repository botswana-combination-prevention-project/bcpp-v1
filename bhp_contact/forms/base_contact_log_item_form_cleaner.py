from django import forms
# from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
# from bhp_contact.choices import INFO_PROVIDER, CONTACT_TYPE


class BaseContactLogItemFormCleaner (object):

#    contact_type = forms.ChoiceField(
#        label='Contact type',
#        choices=[choice for choice in CONTACT_TYPE],
#        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
#        )
#    information_provider = forms.ChoiceField(
#        label='Information provider',
#        choices=[choice for choice in INFO_PROVIDER],
#        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
#        )

    def clean(self, cleaned_data):
        if not cleaned_data.get('is_contacted', None):
            raise forms.ValidationError('Please select Yes or No')
        if cleaned_data.get('is_contacted').lower() == 'no' and cleaned_data.get('information_provider'):
            raise forms.ValidationError('You wrote contact was NOT made yet have recorded the information provider. Please correct.')
        if cleaned_data.get('is_contacted').lower() == 'yes' and not cleaned_data.get('information_provider'):
            raise forms.ValidationError('You wrote contact was made. Please indicate the information provider. Please correct.')
        return cleaned_data
