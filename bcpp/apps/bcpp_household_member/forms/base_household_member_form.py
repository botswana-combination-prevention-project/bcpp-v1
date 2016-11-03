from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm
from edc.core.bhp_common.utils import check_initials_field


class BaseHouseholdMemberForm(BaseModelForm):

    def clean(self):

        cleaned_data = super(BaseHouseholdMemberForm, self).clean()
        household_structure = cleaned_data.get('household_structure', None)
        if household_structure:
            if household_structure.is_dispatched_as_item():
                raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")

        my_initials = cleaned_data.get("initials")
        my_first_name = cleaned_data.get("first_name")
        check_initials_field(my_first_name, None, my_initials)

        return cleaned_data
