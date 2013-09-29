from edc_core.bhp_base_form.forms import BaseModelForm
from ..models import HouseholdLog, HouseholdLogEntry


class HouseholdLogForm(BaseModelForm):

    def clean(self):

        cleaned_data = super(HouseholdLogForm, self).clean()

        return cleaned_data

    class Meta:
        model = HouseholdLog


class HouseholdLogEntryForm(BaseModelForm):

    def clean(self):

        cleaned_data = super(HouseholdLogEntryForm, self).clean()

        return cleaned_data

    class Meta:
        model = HouseholdLogEntry
