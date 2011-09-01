from datetime import date, datetime, timedelta
from django.db.models import Q, Max
from django import forms
from bhp_entry.models import ScheduledEntryBucket


class ScheduledEntryBucketForm (forms.ModelForm): 
    def clean(self):
    
        cleaned_data = self.cleaned_data 
        
        #if entry_status is QUERY, leave a comment
        if cleaned_data['entry_status'] == 'QUERY' and not cleaned_data['entry_comment']:
            raise forms.ValidationError("Entry status has been set to 'QUERY', Please provide a short comment to describe the query")
            
        # if record exists, do not allow 'New':
        if cleaned_data['entry_status'] == 'NEW' cleaned_data['entry_status'] == 'NOT_REQUIRED':
            #query for record
            entry = cleaned_data['entry']                    
            entry.content_type_map.
        
        return cleaned_data
        
    class Meta:
        model = ScheduledEntryBucket 

