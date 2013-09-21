from django import forms
from bhp_base_form.forms import BaseModelForm


class BaseHouseholdMemberForm(BaseModelForm):

    pass

#     def validate_cleaned_data(self, cleaned_data):
# 
#         cleaned_data = self.cleaned_data
#         #check if dispatched. TODO: is this dispatch stuff necessary?
#         household_structure = cleaned_data.get('household_structure', None)
#         first_name = cleaned_data.get("first_name")
# #         if household_structure:
# #             if household_structure.is_dispatched_as_item():
# #                 raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")
#         #check name not repeated
#         if self.model.objects.get(household_structure_id=household_structure, first_name=first_name).exists():
#             raise forms.ValidationError("{0} is already listed as a household member.".format(first_name))
#         return cleaned_data
