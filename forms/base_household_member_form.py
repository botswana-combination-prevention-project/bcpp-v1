from django import forms
from bhp_common.utils import check_initials_field


class BaseHouseholdMemberForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #check if dispatched
        household_structure = cleaned_data.get('household_structure', None)
        if household_structure:
            if household_structure.is_dispatched_as_item():
                raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")
        my_initials = cleaned_data.get("initials")
        my_first_name = cleaned_data.get("first_name")
        check_initials_field(my_first_name, None, my_initials)
        # Always return the full collection of cleaned data.
        return cleaned_data
