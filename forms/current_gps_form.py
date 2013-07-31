from django import forms


class CurrentGpsForm(forms.Form):

    degrees_s = forms.IntegerField(label='DS')
    minutes_s = forms.FloatField(label='MS')
    degrees_e = forms.IntegerField(label='DE')
    minutes_e = forms.FloatField(label='ME')
    radius = forms.DecimalField(label='R (m)')
    community = forms.CharField(widget=forms.HiddenInput())
