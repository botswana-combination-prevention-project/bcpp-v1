from django import forms
from django.core.exceptions import ValidationError
from choices import AGGREGATE


class DateRangeForm(forms.Form):
    
    start_date = forms.DateField(
        label="Start",
        required = False,
        )
    end_date = forms.DateField(
        label="End",
        required = False,
        )
    aggregate_on = forms.ChoiceField(
        label="Aggregate on",
        choices = AGGREGATE,
        initial='month',
        required = False,
        )
        

