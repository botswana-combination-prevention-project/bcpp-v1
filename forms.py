from django import forms


class DispatchForm(forms.Form):
    producer = forms.CharField(max_length=100)
    dispatch_items = forms.Textarea(max_length=500)
