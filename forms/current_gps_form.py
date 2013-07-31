from django import forms


class CurrentGpsForm(forms.Form):

    degrees_s = forms.IntegerField(label='S', required=True)
    minutes_s = forms.IntegerField(label='.', required=True)
    degrees_e = forms.IntegerField(label='E', required=True)
    minutes_e = forms.IntegerField(label='.', required=True)
    radius = forms.DecimalField(label='R (m)', required=True)
    community = forms.CharField(widget=forms.HiddenInput())
