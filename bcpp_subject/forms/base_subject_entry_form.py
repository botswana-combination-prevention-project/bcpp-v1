from django import forms
from edc_lib.bhp_base_form.forms import BaseModelForm


class BaseSubjectEntryForm(BaseModelForm):

    def clean(self):

        cleaned_data = super(BaseSubjectEntryForm, self).clean()
        if cleaned_data.get('next_appt_datetime', None):
            if cleaned_data.get('next_appt_datetime') <= cleaned_data.get('report_datetime'):
                raise forms.ValidationError('Next appointment date must come after the report date. You wrote %s' % (cleaned_data.get('next_appt_datetime'),))
        return cleaned_data
