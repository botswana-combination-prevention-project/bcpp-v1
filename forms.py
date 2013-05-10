from django import forms
from bhp_lab_entry.models import ScheduledLabEntryBucket


class ScheduledLabEntryBucketForm (forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        # if entry_status is QUERY, leave a comment
        if cleaned_data['entry_status'] == 'QUERY' and not cleaned_data['entry_comment']:
            raise forms.ValidationError("Entry status has been set to 'QUERY', Please provide a short comment to describe the query")
        return cleaned_data

    class Meta:
        model = ScheduledLabEntryBucket
