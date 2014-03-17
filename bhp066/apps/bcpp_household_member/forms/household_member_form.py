from django import forms

from base_household_member_form import BaseHouseholdMemberForm
from ..models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    def clean(self):
        cleaned_data = super(HouseholdMemberForm, self).clean()
        # only allow one person to be Head of Household
        household_structure = cleaned_data.get('household_structure')
        initials = cleaned_data.get('initials')
        if cleaned_data.get('eligible_hoh', None):
            if cleaned_data.get('age_in_years', None) < 18:
                raise TypeError('This household member is the head of house. You cannot change their age to less than 18.')
        if cleaned_data.get('relation') == 'Head':
            if HouseholdMember.objects.filter(household_structure=household_structure, relation='Head').exclude(initials=initials):
                household_member = HouseholdMember.objects.get(household_structure=household_structure, relation='Head')
                raise forms.ValidationError('The Head of Household member has already been added. See {0}'.format(household_member))
        return cleaned_data

    class Meta:
        model = HouseholdMember
