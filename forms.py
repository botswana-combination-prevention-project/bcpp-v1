from django import forms
from bhp_entry.models import ScheduledEntryBucket


class ScheduledEntryBucketForm (forms.ModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        if cleaned_data['entry_status'] == 'QUERY' and not cleaned_data['entry_comment']:
            raise forms.ValidationError("Entry status has been set to 'QUERY', Please provide a short comment to describe the query")

        return cleaned_data

    class Meta:
        model = ScheduledEntryBucket
