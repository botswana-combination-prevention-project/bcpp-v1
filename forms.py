from django import forms
from bhp_sync.models import Producer


class DispatchForm(forms.Form):
    producer = forms.ModelChoiceField(queryset=Producer.objects.all().order_by('name'))
    dispatch_items = forms.MultipleChoiceField()
