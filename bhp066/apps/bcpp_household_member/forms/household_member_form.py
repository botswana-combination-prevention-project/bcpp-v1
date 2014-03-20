from django import forms

from ..models import HouseholdMember
from ..classes import HouseholdMemberHelper

from .base_household_member_form import BaseHouseholdMemberForm


class HouseholdMemberForm(BaseHouseholdMemberForm):

    def clean(self):
        household_member_helper = HouseholdMemberHelper()
        household_member_helper.household_member = self.instance
        # only allow one person to be Head of Household
        self.instance.match_eligibility_values(exception_cls=forms.ValidationError)
        household_member_helper.calculate_member_status(exception_cls=forms.ValidationError) # TOD): add exceptions back
#         household_structure = cleaned_data.get('household_structure')
#         initials = cleaned_data.get('initials')
#         if cleaned_data.get('eligible_hoh', None):
#             if cleaned_data.get('age_in_years', None) < 18:
#                 raise TypeError('This household member is the head of house. You cannot change their age to less than 18.')
#         if cleaned_data.get('relation') == 'Head':
#             if HouseholdMember.objects.filter(household_structure=household_structure, relation='Head').exclude(initials=initials):
#                 household_member = HouseholdMember.objects.get(household_structure=household_structure, relation='Head')
#                 raise forms.ValidationError('The Head of Household member has already been added. See {0}'.format(household_member))
        return super(HouseholdMemberForm, self).clean()

    class Meta:
        model = HouseholdMember
