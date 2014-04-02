from django import forms

from ..models import HouseholdMember, EnrollmentChecklist

from .base_household_member_form import BaseHouseholdMemberForm
from ..choices import RELATIONS, FEMALE_RELATIONS, MALE_RELATIONS


class HouseholdMemberForm(BaseHouseholdMemberForm):
    def clean(self):
        cleaned_data = super(HouseholdMemberForm, self).clean()
        self.instance.check_eligible_representative_filled(cleaned_data.get('household_structure', None), forms.ValidationError)
        if cleaned_data.get('relation') == 'Head' and not cleaned_data.get('age_in_years') >= 18:
            raise forms.ValidationError('Head of Household must be 18 years or older.')
        if cleaned_data.get('eligible_hoh') and cleaned_data.get('age_in_years') < 18:
            raise forms.ValidationError('This household member completed the HoH questionnaire. You cannot change their age to less than 18. Got {0}.'.format(cleaned_data.get('age_in_years')))
        if cleaned_data.get('gender') == 'M':
            if cleaned_data.get('relation') not in [item[0] for item in RELATIONS if item not in FEMALE_RELATIONS]:
                raise forms.ValidationError('Member is Male but you selected a female relation. Got {0}.'.format([item[1] for item in RELATIONS if item[0] == cleaned_data.get('relation')][0]))
        if cleaned_data.get('gender') == 'F':
            if cleaned_data.get('relation') not in [item[0] for item in RELATIONS if item not in MALE_RELATIONS]:
                raise forms.ValidationError('Member is Female but you selected a male relation. Got {0}.'.format([item[1] for item in RELATIONS if item[0] == cleaned_data.get('relation')][0]))
        if cleaned_data.get('relation') == 'Head':
            if HouseholdMember.objects.filter(household_structure=cleaned_data.get('household_structure'), relation='Head').exclude(initials=cleaned_data.get('initials')):
                current_hoh = HouseholdMember.objects.get(household_structure=cleaned_data.get('household_structure'), relation='Head')
                raise forms.ValidationError('{0} is the head of household already. Only one member may be the head of household.'.format(current_hoh))
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(household_member=self.instance)
        except:
            enrollment_checklist = None
        if enrollment_checklist:
            enrollment_checklist.matches_household_member_values(enrollment_checklist, HouseholdMember(**cleaned_data), exception_cls=forms.ValidationError)

        return cleaned_data

    class Meta:
        model = HouseholdMember
