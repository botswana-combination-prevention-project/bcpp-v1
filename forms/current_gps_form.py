from django import forms


class CurrentGpsForm(forms.Form):

    degrees_s = forms.IntegerField(label='S')
    minutes_s = forms.FloatField(label='.')
    degrees_e = forms.IntegerField(label='E')
    minutes_e = forms.FloatField(label='.')
    radius = forms.DecimalField(label='R (m)')
    community = forms.CharField(widget=forms.HiddenInput())
