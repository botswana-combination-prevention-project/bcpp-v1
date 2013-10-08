from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import HouseholdLog, HouseholdLogEntry


class HouseholdLogForm(BaseModelForm):

    class Meta:
        model = HouseholdLog


class HouseholdLogEntryForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(HouseholdLogEntryForm, self).clean()
        # confirm next_appt_datetime on on or after report datetime
        if cleaned_data.get('next_appt_datetime'):
            if not cleaned_data.get('next_appt_datetime') >= cleaned_data.get('report_datetime'):
                raise forms.ValidationError('The next appointment date must be on or after the report datetime. You entered {0}'.format(cleaned_data.get('next_appt_datetime').strftime('%Y-%m-%d')))
        return cleaned_data

    class Meta:
        model = HouseholdLogEntry
