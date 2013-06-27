from django import forms
from bcpp_household.models import Ward


class WardForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #Check if there is already a ward with the same name in same village
        village = cleaned_data.get('village_name', None)
        ward = cleaned_data.get('ward_name', None)
        if Ward.objects.filter(village_name=village, ward_name=ward).exists():
            raise forms.ValidationError("There is already a ward named {0} in {1}.".format(ward, village))

        return cleaned_data

    class Meta:
        model = Ward